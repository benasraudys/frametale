# services/ai_narrator.py

import requests
import json
import logging
from typing import List, Dict, Tuple

from core.models import Character
from core import config
from game.tools import TOOL_MAPPING, tools

logger = logging.getLogger(__name__)


def _prepare_system_messages(messages: List[Dict]) -> List[Dict]:
    """Prepares and adds initial system messages to the message history, keeping all but the last two."""
    starting_prompt_content = config.STARTING_PROMPT.format(
        debug_password=config.DEBUG_PASSWORD, story=config.STORY
    )

    # Ensure the initial system message is always present if the history is empty
    if not any(msg.get("role") == "system" for msg in messages):
        messages.insert(0, {"role": "system", "content": starting_prompt_content})

    system_messages = [msg for msg in messages if msg.get("role") == "system"]
    other_messages = [msg for msg in messages if msg.get("role") != "system"]

    # Keep all system messages except the last two
    system_messages_to_keep = (
        system_messages[:-2] if len(system_messages) > 2 else system_messages
    )

    # Reconstruct the messages list with the filtered system messages
    messages_to_keep = []
    system_index = 0
    other_index = 0

    # Merge messages back in their original relative order
    for msg in messages:
        if msg.get("role") == "system":
            if system_index < len(system_messages_to_keep):
                messages_to_keep.append(system_messages_to_keep[system_index])
                system_index += 1
        else:
            if other_index < len(other_messages):
                messages_to_keep.append(other_messages[other_index])
                other_index += 1

    return messages_to_keep


def _prepare_player_state_message(player: Character) -> Dict:
    """Prepares the player state message."""
    player_state_content = f"Player: HP={player.hp}, Stamina={player.stamina}, Money={player.money_oz:.2f}, Location='{player.location}', Inventory=[{', '.join(item.name for item in player.inventory) if player.inventory else 'Empty'}]"
    return {"role": "system", "content": player_state_content}


def _call_ai_api(messages: List[Dict]) -> Dict:
    """Calls the AI API and returns the response data."""
    payload = {
        "model": config.NARRATION_MODEL,
        "messages": messages,
        "tools": tools,
        "tool_choice": "auto",
    }
    headers = {
        "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(config.OPENROUTER_API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()


def _process_ai_response(
    player: Character,
    response_data: Dict,
    messages: List[Dict],
    tool_messages_this_turn: List[str],
) -> Tuple[bool, str]:
    """
    Processes the AI's response, handles tool calls, and updates messages.

    Returns:
        Tuple[bool, str]: A tuple containing:
        - bool: True if tool calls were made, False otherwise.
        - str: The content from the AI response (if any).
    """
    response_message_raw = response_data["choices"][0]["message"]
    response_message = {}
    if isinstance(response_message_raw, dict):
        response_message = response_message_raw
    elif hasattr(response_message_raw, "dict"):  # Handle pydantic models
        response_message = response_message_raw.dict()
    else:
        logger.error(
            f"Unexpected response message format: {type(response_message_raw)}"
        )
        response_message = {
            "role": "assistant",
            "content": str(response_message_raw),
        }  # Default structure

    if response_message.get("content") is None and not response_message.get(
        "tool_calls"
    ):
        response_message["content"] = ""

    messages.append(response_message)

    if response_message.get("tool_calls"):
        logger.info("Tool call requested by LLM.")
        for tool_call in response_message["tool_calls"]:
            tool_name = tool_call["function"]["name"]
            tool_id = tool_call["id"]
            try:
                tool_args = json.loads(tool_call["function"]["arguments"])
                logger.info(f"Executing tool: {tool_name} with args: {tool_args}")

                if tool_name in TOOL_MAPPING:
                    tool_function = TOOL_MAPPING[tool_name]
                    tool_result = tool_function(player, **tool_args)
                    logger.info(f"Tool {tool_name} executed. Result: {tool_result}")

                    if tool_result.get("success") and tool_result.get("message"):
                        tool_messages_this_turn.append(
                            f"[italic yellow]>> {tool_result['message']}[/italic yellow]\n"
                        )

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_id,
                            "name": tool_name,
                            "content": json.dumps(tool_result),
                        }
                    )
                else:
                    logger.error(f"Unknown tool requested: {tool_name}")
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_id,
                            "name": tool_name,
                            "content": json.dumps(
                                {
                                    "success": False,
                                    "error": f"Tool '{tool_name}' not found.",
                                }
                            ),
                        }
                    )
            except json.JSONDecodeError:
                logger.error(
                    f"Failed to decode arguments for tool {tool_name}: {tool_call['function']['arguments']}"
                )
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_id,
                        "name": tool_name,
                        "content": json.dumps(
                            {"success": False, "error": "Invalid arguments format."}
                        ),
                    }
                )
            except Exception as tool_exc:
                logger.exception(f"Error executing tool {tool_name}")
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_id,
                        "name": tool_name,
                        "content": json.dumps(
                            {"success": False, "error": str(tool_exc)}
                        ),
                    }
                )
        return True, ""  # Tool calls were made, continue loop
    else:
        logger.info("No tool calls requested. Yielding content from current response.")
        return False, response_message.get("content", "")


def get_ai_narrative(
    player: Character, prompt: str, messages: List[Dict]
) -> Tuple[str, List[Dict]]:
    """
    Generates narrative using the configured AI API, handling tool calls,
    and returns the final content along with the updated message history.

    Args:
        player: The current player character object.
        prompt: The user's input or the initial prompt.
        messages: The existing message history (will be modified in place).

    Returns:
        A tuple containing:
        - str: The complete AI's narrative response (including tool messages).
        - List[Dict]: The updated message history after this interaction.
    """
    if not config.is_ai_available():
        return (
            "[red]AI Narrator is unavailable due to missing API key.[/red]\n",
            messages,
        )

    messages = _prepare_system_messages(messages)
    messages.append(_prepare_player_state_message(player))
    messages.append({"role": "system", "content": config.REMINDER_MESSAGE})
    messages.append({"role": "user", "content": prompt})

    iteration = 0
    tool_messages_this_turn = []

    try:
        # Summarization logic
        summarization_chunk_size = 5
        unsummarized_message_limit = 10
        user_assistant_messages = [
            msg for msg in messages if msg.get("role") in ["user", "assistant"]
        ]
        if len(user_assistant_messages) > unsummarized_message_limit:
            # Take more to have overlap with summaries (to not miss anything at the edge of transcripts).
            messages_to_summarize = user_assistant_messages[
                : (summarization_chunk_size + 2)
            ]
            summary_prompt = "This is an RPG roleplay transcript of a User (player) and an Assistant (dungeon master). Please write most important facts in a list like this:\nUser saw a giant old building.\nThe building had a familiar graffiti.\nUser went into the building.\nThe giant rat inside the house lunged at him.\n\n---\nDon't say anything else, just list. Be very brief like the examples I showed. Don't use any symbols. List items are separated by new lines only. Here's the transcript:\n\n"
            for msg in messages_to_summarize:
                summary_prompt += (
                    f"{msg.get('role').capitalize()}: {msg.get('content', '')}\n"
                )

            try:
                # Call the AI API for summarization
                summary_payload = {
                    "model": config.SUMMARIZATION_MODEL,
                    "messages": [{"role": "user", "content": summary_prompt}],
                }
                summary_headers = {
                    "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                }
                summary_response = requests.post(
                    config.OPENROUTER_API_URL,
                    headers=summary_headers,
                    json=summary_payload,
                )
                summary_response.raise_for_status()
                summary_data = summary_response.json()
                summary_content = summary_data["choices"][0]["message"]["content"]

                # Find the indices of the messages to remove from the original messages list
                original_indices_to_remove = []
                user_assistant_count = 0
                for i, msg in enumerate(messages):
                    if (
                        msg.get("role") in ["user", "assistant"]
                        and user_assistant_count < summarization_chunk_size
                    ):
                        original_indices_to_remove.append(i)
                        user_assistant_count += 1
                    if user_assistant_count == summarization_chunk_size:
                        break

                # Remove original messages in reverse order to avoid index issues
                for index in sorted(original_indices_to_remove, reverse=True):
                    messages.pop(index)  # 123

                # Insert the summary message at the position of the first removed message
                insert_index = (
                    original_indices_to_remove[0] if original_indices_to_remove else 0
                )
                messages.insert(
                    insert_index,
                    {
                        "role": "system",
                        "content": f"Summary: {summary_content.strip()}",
                    },
                )
                logger.info(
                    f"Summarized first {user_assistant_count} user/assistant messages using LLM."
                )

            except requests.exceptions.RequestException as e:
                logger.error(f"Error calling AI API for summarization: {e}")
                # Continue without summarization if API call fails
            except Exception as e:
                logger.exception("Error during summarization.")
                # Continue without summarization if summarization fails

        while iteration < config.MAX_TOOL_ITERATIONS:
            iteration += 1
            logger.debug(f"--- AI Call Iteration {iteration} ---")
            logger.debug(
                f"Messages sent (last 2): {json.dumps(messages[-2:], indent=2)}"
            )

            response_data = _call_ai_api(messages)
            tool_calls_made, final_content = _process_ai_response(
                player, response_data, messages, tool_messages_this_turn
            )

            if not tool_calls_made:
                final_narrative = (
                    "\n".join(tool_messages_this_turn) + final_content
                    if tool_messages_this_turn
                    else final_content
                )
                return final_narrative, messages

        # --- Loop finished (Max iterations reached) ---
        logger.warning(f"Max tool iterations ({config.MAX_TOOL_ITERATIONS}) reached.")
        last_message = messages[-1] if messages else {}
        if last_message.get("role") == "assistant" and last_message.get("content"):
            final_narrative = (
                "\n".join(tool_messages_this_turn) + last_message["content"]
                if tool_messages_this_turn
                else last_message["content"]
            )
            return final_narrative, messages
        else:
            final_narrative = (
                "\n".join(tool_messages_this_turn)
                if tool_messages_this_turn
                else "[italic yellow]>> The story seems paused after complex actions. Please provide your next action.[/italic yellow]\n"
            )
            return final_narrative, messages

    except requests.exceptions.RequestException as e:
        error_message = f"Error calling AI API: {e}"
        logger.error(error_message)
        return (
            f"[bold red]Error communicating with AI Narrator: {e}[/bold red]\n",
            messages,
        )
    except Exception as e:
        error_message = f"Error in AI narrative generation: {e}"
        logger.exception("Error in AI narrative generation.")
        return f"[bold red]Error processing AI narrative: {e}[/bold red]\n", messages
