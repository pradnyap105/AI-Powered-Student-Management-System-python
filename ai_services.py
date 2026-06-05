from openai import OpenAI

client = OpenAI()

def generate_feedback(student):

    prompt = f"""
    Student Name: {student.name}
    Course: {student.course}
    Marks: {student.marks}

    Generate improvement feedback.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content