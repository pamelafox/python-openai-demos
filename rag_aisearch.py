import os

import openai
from dotenv import load_dotenv

# Setup the OpenAI client to use either Azure, OpenAI.com, or Ollama API
load_dotenv(override=True)

client = openai.OpenAI(base_url="https://models.inference.ai.azure.com", api_key=os.getenv("GITHUB_TOKEN"))
MODEL_NAME = "DeepSeek-R1"


# Not supported: temperature, top_p, tools
# max_tokens is supported BUT that may end up cutting off a thought process!
# stop is also supported
completion = client.chat.completions.create(
    model=MODEL_NAME,
    n=1,
    messages=[{
        "role": "user",
        "content": "Assistant helps the company employees with their healthcare plan questions, and questions about the employee handbook. Be brief in your answers.\nAnswer ONLY with the facts listed in the list of sources below. If there isn't enough information below, say you don't know. Do not generate answers that don't use the sources below. If asking a clarifying question to the user would help, ask the question.\nIf the question is not in English, answer in the language used in the question.\nEach source has a name followed by colon and the actual information, always include the source name for each fact you use in the response. Use square brackets to reference the source, for example [info1.txt]. Don't combine sources, list each source separately, for example [info1.txt][info2.pdf].\n\n\nWhat is included in my Northwind Health Plus plan that is not in standard?\n\nSources:\n\nBenefit_Options.pdf#page=3:  With Northwind Health Plus, you can choose from a variety of in-network providers, including primary care physicians, specialists, hospitals, and pharmacies. This plan also offers coverage for emergency services, both in-network and out-of-network. Northwind Standard Northwind Standard is a basic plan that provides coverage for medical, vision, and dental services. This plan also offers coverage for preventive care services, as well as prescription drug coverage. With Northwind Standard, you can choose from a variety of in-network providers, including primary care physicians, specialists, hospitals, and pharmacies. This plan does not offer coverage for emergency services, mental health and substance abuse coverage, or out-of-network services. Comparison of Plans Both plans offer coverage for routine physicals, well-child visits, immunizations, and other preventive care services. The plans also cover preventive care services such as mammograms, colonoscopies, and other cancer screenings. Northwind Health Plus offers more comprehensive coverage than Northwind Standard.\n\nNorthwind_Standard_Benefits_Details.pdf#page=45:  With Northwind Standard, you can take advantage of these important services, which are covered at no additional cost.Remember, preventive care is an important part of your overall health. Northwind Health is dedicated to helping you get the preventive care you need to stay healthy and protect yourself for the future. Professional Visits And Services COVERED SERVICES: Professional Visits and Services Northwind Standard provides coverage for professional visits and services. This includes visits to your primary care physician, specialists, and other health care providers. This coverage is available for services that are medically necessary and are provided by in- network providers. In-network providers will generally provide services at a lower cost than out-of-network providers, so it is important to check with Northwind Health before making an appointment to ensure that the provider is in-network. This can help you save money and avoid unexpected costs. The Northwind Standard plan covers services such as: - Preventive care services, including physicals, immunizations, and screenings - Diagnostic \n\nBenefit_Options.pdf#page=3:  Both plans offer coverage for medical services. Northwind Health Plus offers coverage for hospital stays, doctor visits, lab tests, and X-rays. Northwind Standard only offers coverage for doctor visits and lab tests. Northwind Health Plus is a comprehensive plan that offers more coverage than Northwind Standard. Northwind Health Plus offers coverage for emergency services, mental health and substance abuse coverage, and out-of-network services, while Northwind Standard does not. Northwind Health Plus alsooffers a wider range of prescription drug coverage than Northwind Standard. Both plans offer coverage for vision and dental services, as well as medical services. Cost Comparison Contoso Electronics deducts the employee's portion of the healthcare cost from each paycheck. This means that the cost of the health insurance will be spread out over the course of the year, rather than being paid in one lump sum. The employee's portion of the cost will be calculated based on the selected health plan and the number of people covered by the insurance."
    }],
    stream=True
)

print("Response: ")
is_thinking = False
for event in completion:
    if event.choices:
        content = event.choices[0].delta.content
        if content == "<think>":
            is_thinking = True
            # note: this is sometimes followed ONLY by a new line
            print("🧠 Thinking...", end="", flush=True)
        elif content == "</think>":
            is_thinking = False
            print("🛑\n\n")
        elif content:
            print(content, end="", flush=True)
