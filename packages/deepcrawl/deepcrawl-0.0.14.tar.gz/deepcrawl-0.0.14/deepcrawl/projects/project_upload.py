"""
Project Upload
================
"""

from deepcrawl.utils import ImmutableAttributesMixin
from deepcrawl.utils import safe_string_to_datetime

project_upload_extra_fields = (
    "id",
    "account_id",
    "project_id",
)

project_upload_mutable_fields = (
    "enabled",
)

project_upload_immutable_fields = (
    "created_at",
    "status",
    "file_name",
    "total_rows",
    "project_upload_file",
    "project_upload_type",
    "crawl_type",
    "upload_base_domain",
    "processing_feedback",
    "custom_upload_template",
    "custom_type",
    "is_customizable",
)

project_upload_fields = project_upload_extra_fields + project_upload_mutable_fields + project_upload_immutable_fields


class DeepCrawlProjectUpload(ImmutableAttributesMixin):
    """
    Project Upload class
    """
    __slots__ = project_upload_fields

    mutable_attributes = project_upload_mutable_fields

    def __init__(self, project_upload_data: dict, account_id, project_id):
        self.id = project_upload_data.get("id")
        self.account_id = account_id
        self.project_id = project_id

        self.created_at = safe_string_to_datetime(project_upload_data.get("created_at"))
        self.enabled = project_upload_data.get("enabled")
        self.status = project_upload_data.get("status")
        self.file_name = project_upload_data.get("file_name")
        self.total_rows = project_upload_data.get("total_rows")
        self.project_upload_file = project_upload_data.get("project_upload_file")
        self.project_upload_type = project_upload_data.get("project_upload_type")
        self.crawl_type = project_upload_data.get("crawl_type")
        self.upload_base_domain = project_upload_data.get("upload_base_domain")
        self.processing_feedback = project_upload_data.get("processing_feedback")
        self.custom_upload_template = project_upload_data.get("custom_upload_template")
        self.custom_type = project_upload_data.get("custom_type")
        self.is_customizable = project_upload_data.get("is_customizable")

        super(DeepCrawlProjectUpload, self).__init__()

    def __str__(self):
        return f"[{self.account_id} {self.project_id}] {self.file_name}"

    def __repr__(self):
        return f"[{self.account_id} {self.project_id}] {self.file_name}"

    @property
    def to_dict_mutable_fields(self):
        """
        :return: dictionary with the mutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in project_upload_mutable_fields}

    @property
    def to_dict_immutable_fields(self):
        """
        :return: dictionary with the immutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in project_upload_immutable_fields}
