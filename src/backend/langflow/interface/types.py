from langflow.interface.agents.base import agent_creator
from langflow.interface.chains.base import chain_creator
from langflow.interface.document_loaders.base import documentloader_creator
from langflow.interface.embeddings.base import embedding_creator
from langflow.interface.llms.base import llm_creator
from langflow.interface.memories.base import memory_creator
from langflow.interface.prompts.base import prompt_creator
from langflow.interface.text_splitters.base import textsplitter_creator
from langflow.interface.toolkits.base import toolkits_creator
from langflow.interface.tools.base import tool_creator
from langflow.interface.utilities.base import utility_creator
from langflow.interface.vector_store.base import vectorstore_creator
from langflow.interface.wrappers.base import wrapper_creator

from langflow.template.field.base import TemplateField
from langflow.template.frontend_node.tools import CustomComponentNode


def get_type_list():
    """Get a list of all langchain types"""
    all_types = build_langchain_types_dict()

    # all_types.pop("tools")

    for key, value in all_types.items():
        all_types[key] = [item["template"]["_type"] for item in value.values()]

    return all_types


def build_langchain_types_dict():  # sourcery skip: dict-assign-update-to-union
    """Build a dictionary of all langchain types"""

    all_types = {}

    creators = [
        chain_creator,
        agent_creator,
        prompt_creator,
        llm_creator,
        memory_creator,
        tool_creator,
        toolkits_creator,
        wrapper_creator,
        embedding_creator,
        vectorstore_creator,
        documentloader_creator,
        textsplitter_creator,
        utility_creator,
    ]

    all_types = {}
    for creator in creators:
        created_types = creator.to_dict()
        if created_types[creator.type_name].values():
            all_types.update(created_types)
    return all_types


# TODO: Move to correct place
def find_class_type(class_name, classes_dict):
    return next(
        (
            {"type": class_type, "class": class_name}
            for class_type, class_list in classes_dict.items()
            if class_name in class_list
        ),
        {"error": "class not found"},
    )


# TODO: Move to correct place
def add_new_custom_field(template, field_name: str, field_type: str):
    new_field = TemplateField(
        name=field_name,
        field_type=field_type,
        show=True,
        advanced=False
    )
    template.get('template')[field_name] = new_field.to_dict()
    template.get('custom_fields').append(field_name)

    return template

# TODO: Move to correct place


def add_code_field(template, raw_code):
    # Field with the Python code to allow update
    code_field = {
        "code": {
            "required": True,
            "placeholder": "",
            "show": True,
            "multiline": True,
            "value": raw_code,
            "password": False,
            "name": "code",
            "advanced": False,
            "type": "code",
            "list": False
        }
    }
    template.get('template')['code'] = code_field.get('code')

    return template


def build_langchain_template_custom_component(raw_code, function_args, function_return_type):
    # type_list = get_type_list()
    # type_and_class = find_class_type("Tool", type_list)
    # node = get_custom_nodes(node_type: str)

    # TODO: Build base template
    template = llm_creator.to_dict()['llms']['ChatOpenAI']

    template = CustomComponentNode().to_dict().get('CustomComponent')

    # TODO: Add extra fields
    template = add_new_custom_field(
        template,
        "my_id",
        "str"
    )

    template = add_new_custom_field(
        template,
        "year",
        "int"
    )

    template = add_new_custom_field(
        template,
        "other_field",
        "bool"
    )

    template = add_code_field(
        template,
        raw_code
    )

    # criar um vertex
    # olhar loading.py

    return template
    # return globals()['tool_creator'].to_dict()[type_and_class['type']][type_and_class['class']]
    # return chain_creator.to_dict()['chains']['ConversationChain']
