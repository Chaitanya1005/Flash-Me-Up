import json
from groq import Groq
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

client = Groq(
    api_key=settings.GROQ_API_KEY,
)

def generate_flashcards(text_chunk: str) -> list[dict]:
    """
    Given a text chunk, uses OpenAI to generate flashcards.
    Returns a list of dicts: {"question": "", "answer": "", "difficulty_level": "", "topic": ""}
    """
    prompt = f"""
    You are an expert educator. Extract the key concepts from the following text and convert them into high-quality flashcards.
    Prioritize conceptual clarity and avoid generic cards.
    
    Each flashcard must contain:
    - question
    - answer
    - difficulty_level (easy, medium, hard)
    - topic (a very short tag)

    Return the output STRICTLY as a JSON object with a single root key 'flashcards' containing an array of these objects.
    Do not include markdown formatting or any other text.
    
    Text:
    {text_chunk}
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates JSON flashcards."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
        )
        
        content = response.choices[0].message.content
        parsed = json.loads(content.strip())
        if isinstance(parsed, dict) and 'flashcards' in parsed:
            return parsed['flashcards']
        elif isinstance(parsed, list):
            return parsed
        return []
    except Exception as e:
        logger.error(f"Failed to generate flashcards (likely missing API key), falling back to mock: {e}")
        return [
            {
                "question": "What is Spaced Repetition (SRS)?",
                "answer": "An evidence-based learning technique that incorporates increasing intervals of time between subsequent review of previously learned material.",
                "difficulty_level": "medium",
                "topic": "Learning Science"
            },
            {
                "question": "Why is the SM-2 algorithm significant?",
                "answer": "Created for SuperMemo in the 1980s, it calculates the optimum intervals between study sessions based on the user's recall quality (often graded 1-5).",
                "difficulty_level": "hard",
                "topic": "Algorithms"
            },
            {
                "question": "What is the primary benefit of Fast Retrieval?",
                "answer": "It minimizes the user's cognitive wait-time, keeping them in a state of \"flow\" while studying.",
                "difficulty_level": "easy",
                "topic": "UX Design"
            }
        ]
