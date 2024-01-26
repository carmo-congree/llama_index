from typing import Callable, Optional

from llama_index.bridge.pydantic import BaseModel
from llama_index.callbacks.base import CallbackManager
from llama_index.indices.prompt_helper import PromptHelper
from llama_index.llm_predictor.base import LLMPredictorType
from llama_index.prompts import BasePromptTemplate
from llama_index.prompts.default_prompt_selectors import (
    DEFAULT_REFINE_PROMPT_SEL,
    DEFAULT_TEXT_QA_PROMPT_SEL,
    DEFAULT_TREE_SUMMARIZE_PROMPT_SEL,
)
from llama_index.prompts.default_prompts import DEFAULT_SIMPLE_INPUT_PROMPT
from llama_index.prompts.prompts import PromptTemplate
from llama_index.response_synthesizers.accumulate import Accumulate
from llama_index.response_synthesizers.base import BaseSynthesizer
from llama_index.response_synthesizers.compact_and_accumulate import (
    CompactAndAccumulate,
)
from llama_index.response_synthesizers.compact_and_refine import CompactAndRefine
from llama_index.response_synthesizers.generation import Generation
from llama_index.response_synthesizers.no_text import NoText
from llama_index.response_synthesizers.refine import Refine
from llama_index.response_synthesizers.simple_summarize import SimpleSummarize
from llama_index.response_synthesizers.tree_summarize import TreeSummarize
from llama_index.response_synthesizers.type import ResponseMode
from llama_index.service_context import ServiceContext
from llama_index.settings import (
    Settings,
    callback_manager_from_settings_or_context,
    llm_from_settings_or_context,
    prompt_helper_from_settings_or_context,
)
from llama_index.types import BasePydanticProgram


def get_response_synthesizer(
    llm: Optional[LLMPredictorType] = None,
    prompt_helper: Optional[PromptHelper] = None,
    service_context: Optional[ServiceContext] = None,
    text_qa_template: Optional[BasePromptTemplate] = None,
    refine_template: Optional[BasePromptTemplate] = None,
    summary_template: Optional[BasePromptTemplate] = None,
    simple_template: Optional[BasePromptTemplate] = None,
    response_mode: ResponseMode = ResponseMode.COMPACT,
    callback_manager: Optional[CallbackManager] = None,
    use_async: bool = False,
    streaming: bool = False,
    structured_answer_filtering: bool = False,
    output_cls: Optional[BaseModel] = None,
    program_factory: Optional[Callable[[PromptTemplate], BasePydanticProgram]] = None,
    verbose: bool = False,
) -> BaseSynthesizer:
    """Get a response synthesizer."""
    text_qa_template = text_qa_template or DEFAULT_TEXT_QA_PROMPT_SEL
    refine_template = refine_template or DEFAULT_REFINE_PROMPT_SEL
    simple_template = simple_template or DEFAULT_SIMPLE_INPUT_PROMPT
    summary_template = summary_template or DEFAULT_TREE_SUMMARIZE_PROMPT_SEL

    callback_manager = callback_manager or callback_manager_from_settings_or_context(
        Settings, service_context
    )
    llm = llm or llm_from_settings_or_context(Settings, service_context)
    prompt_helper = prompt_helper or prompt_helper_from_settings_or_context(
        Settings, service_context
    )

    if response_mode == ResponseMode.REFINE:
        return Refine(
            llm=llm,
            callback_manager=callback_manager,
            prompt_helper=prompt_helper,
            text_qa_template=text_qa_template,
            refine_template=refine_template,
            output_cls=output_cls,
            streaming=streaming,
            structured_answer_filtering=structured_answer_filtering,
            program_factory=program_factory,
            verbose=verbose,
            # deprecated
            service_context=service_context,
        )
    elif response_mode == ResponseMode.COMPACT:
        return CompactAndRefine(
            llm=llm,
            callback_manager=callback_manager,
            prompt_helper=prompt_helper,
            text_qa_template=text_qa_template,
            refine_template=refine_template,
            output_cls=output_cls,
            streaming=streaming,
            structured_answer_filtering=structured_answer_filtering,
            program_factory=program_factory,
            verbose=verbose,
            # deprecated
            service_context=service_context,
        )
    elif response_mode == ResponseMode.TREE_SUMMARIZE:
        return TreeSummarize(
            llm=llm,
            callback_manager=callback_manager,
            prompt_helper=prompt_helper,
            summary_template=summary_template,
            output_cls=output_cls,
            streaming=streaming,
            use_async=use_async,
            verbose=verbose,
            # deprecated
            service_context=service_context,
        )
    elif response_mode == ResponseMode.SIMPLE_SUMMARIZE:
        return SimpleSummarize(
            llm=llm,
            callback_manager=callback_manager,
            prompt_helper=prompt_helper,
            text_qa_template=text_qa_template,
            streaming=streaming,
            # deprecated
            service_context=service_context,
        )
    elif response_mode == ResponseMode.GENERATION:
        return Generation(
            llm=llm,
            callback_manager=callback_manager,
            prompt_helper=prompt_helper,
            simple_template=simple_template,
            streaming=streaming,
            # deprecated
            service_context=service_context,
        )
    elif response_mode == ResponseMode.ACCUMULATE:
        return Accumulate(
            llm=llm,
            callback_manager=callback_manager,
            prompt_helper=prompt_helper,
            text_qa_template=text_qa_template,
            output_cls=output_cls,
            streaming=streaming,
            use_async=use_async,
            # deprecated
            service_context=service_context,
        )
    elif response_mode == ResponseMode.COMPACT_ACCUMULATE:
        return CompactAndAccumulate(
            llm=llm,
            callback_manager=callback_manager,
            prompt_helper=prompt_helper,
            text_qa_template=text_qa_template,
            output_cls=output_cls,
            streaming=streaming,
            use_async=use_async,
            # deprecated
            service_context=service_context,
        )
    elif response_mode == ResponseMode.NO_TEXT:
        return NoText(
            streaming=streaming,
            callback_manager=callback_manager,
            prompt_helper=prompt_helper,
            # deprecated
            service_context=service_context,
        )
    else:
        raise ValueError(f"Unknown mode: {response_mode}")
