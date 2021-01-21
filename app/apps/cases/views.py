import logging

from apps.camunda.serializers import CamundaTaskSerializer
from apps.camunda.services import CamundaService
from apps.cases.filters import CaseFilter
from apps.cases.mock import mock_cases
from apps.cases.models import Case, CaseState, CaseTeam
from apps.cases.serializers import (
    CaseReasonSerializer,
    CaseSerializer,
    CaseStateSerializer,
    CaseTeamSerializer,
    PushCaseStateSerializer,
)
from apps.debriefings.mixins import DebriefingsMixin
from apps.events.mixins import CaseEventsMixin
from apps.users.auth_apps import TopKeyAuth
from django.conf import settings
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from keycloak_oidc.drf.permissions import IsInAuthorizedRealm
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

logger = logging.getLogger(__name__)


class CaseStateViewSet(ViewSet):
    """
    Pushes the case state
    """

    permission_classes = [IsInAuthorizedRealm | TopKeyAuth]
    serializer_class = CaseStateSerializer

    @action(
        detail=True,
        url_path="update-from-top",
        methods=["post"],
        serializer_class=PushCaseStateSerializer,
    )
    def update_from_top(self, request, pk):
        logger.info("Receiving pushed state update")
        data = request.data
        serializer = self.serializer_class(data=data)

        if not serializer.is_valid():
            logger.error("Serializer error: {serializer.errors}")
            raise APIException(f"Serializer error: {serializer.errors}")

        try:
            case_state = CaseState.objects.get(id=pk)
            case_state.users.clear()
            user_emails = data.get("user_emails", [])
            logger.info(f"Updating CaseState {len(user_emails)} users")
            user_model = get_user_model()

            for user_email in user_emails:
                user_object, _ = user_model.objects.get_or_create(email=user_email)
                case_state.users.add(user_object)
                logger.info("Added user to CaseState")

            return Response(CaseStateSerializer(case_state).data)
        except Exception as e:
            logger.error(f"Could not process push data: {e}")
            raise logger(f"Could not push data: {e}")


class CaseViewSet(
    ViewSet,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    DebriefingsMixin,
    CaseEventsMixin,
):
    serializer_class = CaseSerializer
    queryset = Case.objects.all()
    filterset_class = CaseFilter

    @action(detail=False, methods=["post"], url_path="generate-mock")
    def mock_cases(self, request):
        try:
            assert (
                settings.DEBUG or settings.ENVIRONMENT == "acceptance"
            ), "Incorrect enviroment"
            mock_cases()
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

    @extend_schema(
        description="Get Camunda tasks for this Case",
        responses={status.HTTP_200_OK: CamundaTaskSerializer(many=True)},
    )
    @action(detail=True, methods=["get"], url_path="tasks")
    def get_tasks(self, request, pk):
        case = self.get_object()
        camunda_tasks = CamundaService().get_all_tasks_by_instance_id(case.camunda_id)

        if camunda_tasks:
            serializer = CamundaTaskSerializer(camunda_tasks, many=True)

            return Response(serializer.data)
        return Response([])


class CaseTeamViewSet(ViewSet, ListAPIView):
    serializer_class = CaseTeamSerializer
    queryset = CaseTeam.objects.all()

    @extend_schema(
        description="Gets the reasons associated with the requested team",
        responses={status.HTTP_200_OK: CaseReasonSerializer(many=True)},
    )
    @action(
        detail=True,
        url_path="reasons",
        methods=["get"],
    )
    def reasons(self, request, pk):
        paginator = PageNumberPagination()
        case_team = self.get_object()
        query_set = case_team.case_reasons.all()

        context = paginator.paginate_queryset(query_set, request)
        serializer = CaseReasonSerializer(context, many=True)

        return paginator.get_paginated_response(serializer.data)
