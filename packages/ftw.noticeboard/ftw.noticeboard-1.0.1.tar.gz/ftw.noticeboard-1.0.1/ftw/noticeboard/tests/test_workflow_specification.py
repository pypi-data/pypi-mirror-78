from ftw.lawgiver.tests.base import WorkflowTest
from ftw.noticeboard.testing import NOTICEBOARD_FUNCTIONAL


class TestBernWorkflowSpecification(WorkflowTest):
    layer = NOTICEBOARD_FUNCTIONAL
    workflow_path = '../profiles/default/workflows/noticeboard_workflow'
