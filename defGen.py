import vertexai
from vertexai.preview.language_models import TextGenerationModel

def predict_large_language_model(
    content: str,
    project_id: str = "auxiliary-projects",
    model_name: str = "text-bison@001",
    temperature: float = 0.2,
    max_decode_steps: int = 256,
    top_p: float = 0.8,
    top_k: int = 40,
    location: str = "us-central1",
    tuned_model_name: str = "",
    ) :
    """Predict using a Large Language Model."""
    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained(model_name)
    if tuned_model_name:
      model = model.get_tuned_model(tuned_model_name)
    header = '''Glossary of brief definitions of academic concepts.

concept: API Application Programming Interface (Computer Science / Software Engineering)
definitio: Set of protocols, routines and tools for software that specify how components interact with each other. It is a way to exchange data between applications.
The most common types of APIs are REST, SOAP and GraphQL.

concept: TLS Transport Layer Security (Computer Science / Networks)
definition: Protocol used to secure communication over the internet. It provides encryption and authentication between two endpoints, typically a client and a server. TLS works by establishing a secure connection between the two parties, using a combination of symmetric and asymmetric cryptography to ensure confidentiality and integrity of the data being transmitted.

concept: DOM Document Object Model (Computer Science / Software Engineering)
definitio: Programming interface for web documents. It represents the page so that programs can change the document structure, style, and content. The DOM represents the document as nodes and objects, allowing programs to dynamically access and manipulate the content, structure, and style of the document. The DOM is platform and language independent, making it an essential component of web development.

concept: Class Diagram (Computer Science / Software Engineering)
definition: A graphical representation of the structure of a class in object-oriented programming. It shows the classes, their attributes, and the relationships between them. Class diagrams are used to model the design of a software system and to communicate it to other developers.
'''
    response = model.predict(
        header+content,
        temperature=temperature,
        max_output_tokens=max_decode_steps,
        top_k=top_k,
        top_p=top_p,)
    print(f"Response from Model: {response.text}")
    return response.text[12:]