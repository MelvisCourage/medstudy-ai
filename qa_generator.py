import anthropic
import json
import re

def generate_qa(pdf_text: str, num_questions: int, subject: str, api_key: str) -> list[tuple[str, str]]:
    """
    Send PDF text to Claude and get back exam-style Q&A pairs.
    Returns a list of (question, answer) tuples.
    """
    client = anthropic.Anthropic(api_key=api_key)

    # Chunk text if too long (Claude has context limits)
    max_chars = 80000
    if len(pdf_text) > max_chars:
        pdf_text = pdf_text[:max_chars] + "\n\n[Text truncated due to length]"

    subject_note = f"The subject is {subject}." if subject else ""

    prompt = f"""You are an expert medical examiner creating exam questions strictly based on the provided lecture handout.

{subject_note}

INSTRUCTIONS:
- Generate exactly {num_questions} exam-style questions with answers
- Base EVERY question and answer ONLY on the content in the handout below
- Do NOT use any external knowledge
- Answers should be concise and exam-appropriate (2-5 sentences)
- Cover different topics from across the entire handout
- Mix question types: definitions, mechanisms, clinical significance, classifications, comparisons

Return your response as a JSON array like this:
[
  {{"question": "What is X?", "answer": "X is..."}},
  {{"question": "Describe the mechanism of Y.", "answer": "The mechanism involves..."}}
]

Return ONLY the JSON array. No preamble, no explanation, no markdown code fences.

HANDOUT CONTENT:
{pdf_text}
"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip()

    # Clean up any accidental markdown fences
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    raw = raw.strip()

    try:
        data = json.loads(raw)
        return [(item["question"], item["answer"]) for item in data if "question" in item and "answer" in item]
    except Exception as e:
        print(f"JSON parse error: {e}")
        print(f"Raw output: {raw[:500]}")
        return []
