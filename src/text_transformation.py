import sys
from openai import OpenAI
import os


def transform_text(text):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    response = client.chat.completions.create(model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": """
        Rewrite the following transcript as if you are a friendly, experienced, 60-year-old caucasian plain Midwestern pilot. 
        Use casual, warm phrasing with a calm and reassuring tone. Toss in a few classic pilot-isms. 
        
        Your rewrite should not include anything ethnic or related to anything but things white people enjoy mentioned in the original text.
        This includes movies, music, food, and other things.
        
        Here are some examples of how the transcript should be rewritten:
        
        Original: Hi y'all, this is Cleveland. 
        Pilot: Good afternoon, folks, this is Captain Dale Clark up here in the flight deck.
        
        Original: We're way up in the air. 
        Pilot: We've reached our cruising altitude of 37,000 feet.
        
        Original: Y'all get ready to watch Big Momma's House. 
        Pilot: Our in-flight entertainment today will be Under the Tuscan Sun.
        
        Only respond with the rewritten text. Do not include any other information or disclaimers. Keep the number of sentences the same as the original transcript.
        """
        },
        {"role": "user", "content": text},
    ],
    temperature=0.8,
    max_tokens=500)

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python text_transformation.py [input_text_file] [optional_output_file]"
        )
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "transformed.txt"

    with open(input_file, "r", encoding="utf-8") as f:
        input_text = f.read()

    output_text = transform_text(input_text)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output_text)

    print(f"Transformed text saved to: {output_file}")
