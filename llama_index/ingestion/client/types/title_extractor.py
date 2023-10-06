# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ..core.datetime_utils import serialize_datetime
from .llm_predictor import LlmPredictor
from .metadata_mode import MetadataMode


class TitleExtractor(pydantic.BaseModel):
    """
    Title extractor. Useful for long documents. Extracts `document_title`
    metadata field.

    Args:
        llm_predictor (Optional[LLMPredictor]): LLM predictor
        nodes (int): number of nodes from front to use for title extraction
        node_template (str): template for node-level title clues extraction
        combine_template (str): template for combining node-level clues into
            a document-level title
    """

    is_text_node_only: typing.Optional[bool]
    show_progress: typing.Optional[bool] = pydantic.Field(
        description="Whether to show progress."
    )
    metadata_mode: typing.Optional[MetadataMode] = pydantic.Field(
        description="Metadata mode to use when reading nodes."
    )
    node_text_template: typing.Optional[str] = pydantic.Field(
        description="Template to represent how node text is mixed with metadata text."
    )
    disable_template_rewrite: typing.Optional[bool] = pydantic.Field(
        description="Disable the node template rewrite."
    )
    in_place: typing.Optional[bool] = pydantic.Field(
        description="Whether to process nodes in place."
    )
    llm_predictor: LlmPredictor = pydantic.Field(
        description="The LLMPredictor to use for generation."
    )
    nodes: typing.Optional[int] = pydantic.Field(
        description="The number of nodes to extract titles from."
    )
    node_template: typing.Optional[str] = pydantic.Field(
        description="The prompt template to extract titles with."
    )
    combine_template: typing.Optional[str] = pydantic.Field(
        description="The prompt template to merge titles with."
    )
    class_name: typing.Optional[str]

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {
            "by_alias": True,
            "exclude_unset": True,
            **kwargs,
        }
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {
            "by_alias": True,
            "exclude_unset": True,
            **kwargs,
        }
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        json_encoders = {dt.datetime: serialize_datetime}
