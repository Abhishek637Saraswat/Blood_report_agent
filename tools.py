## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai_tools import SerperDevTool
from crewai.tools import BaseTool
from langchain_community.document_loaders import PyPDFLoader as PDFLoader


## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
class ReadBloodTestPDFTool(BaseTool):
    name: str = "Read Blood Test PDF"
    description: str = "Reads and returns the content of a blood test PDF file."

    def _run(self, path='data/sample.pdf'):
        docs = PDFLoader(file_path=path).load()
        full_report = ""
        for data in docs:
            content = data.page_content
            while "\n\n" in content:
                content = content.replace("\n\n", "\n")
            full_report += content + "\n"
        return full_report


class NutritionListTool(BaseTool):
    name: str = "Nutrition List Tool"
    description: str = (
        "Returns a comprehensive nutrition list including essential vitamins, minerals, macronutrients, "
        "and dietary tips for general health. Use as a reference to suggest appropriate nutrition based on patient condition."
    )

    def _run(self) -> str:
        return """
=== Comprehensive Nutrition Reference List ===

**Macronutrients**
- **Proteins:** Lean meats, fish, eggs, dairy, legumes, tofu, nuts. Supports tissue repair and immune function.
- **Carbohydrates:** Whole grains, brown rice, oats, sweet potatoes, fruits. Primary energy source.
- **Fats:** Olive oil, avocados, seeds, nuts, fatty fish. Important for cell health and hormone balance.

**Vitamins**
- **Vitamin A:** Carrots, sweet potatoes, spinach, kale. Vision and immune health.
- **Vitamin B12:** Fish, meat, dairy, eggs, fortified cereals. Nerve and blood cell health.
- **Vitamin C:** Citrus, strawberries, bell peppers, broccoli. Antioxidant and skin health.
- **Vitamin D:** Sunlight, oily fish, eggs, fortified milk. Bone and immune health.
- **Vitamin E:** Nuts, seeds, spinach, sunflower oil. Antioxidant.

**Minerals**
- **Iron:** Red meat, spinach, lentils, pumpkin seeds. Prevents anemia.
- **Calcium:** Dairy, leafy greens, tofu, almonds. Bone and dental health.
- **Magnesium:** Nuts, beans, whole grains, dark chocolate. Muscle and nerve function.
- **Zinc:** Meat, legumes, pumpkin seeds, nuts. Immunity and wound healing.
- **Potassium:** Bananas, oranges, potatoes, beans. Blood pressure and heart health.

**Fiber**
- Fruits, vegetables, whole grains, legumes. Digestive health.

**Hydration**
- Drink 2–3 liters of water daily.

**Other Tips**
- Eat a colorful variety of fruits and vegetables every day.
- Limit processed foods, excess sugar, and sodium.
- Adjust portions and nutrients for age, activity, and health status.

*Agent: Use this list to pick relevant nutrients and foods for the patient's condition, not as a diagnosis!*
""".strip()


class ExerciseListTool(BaseTool):
    name: str = "Exercise List Tool"
    description: str = (
        "Returns a comprehensive list of exercise types and recommendations. Use as a reference to create personalized fitness advice."
    )

    def _run(self) -> str:
        return """
=== Comprehensive Exercise Reference List ===

**Cardiovascular/Aerobic**
- Walking, jogging, running, cycling, swimming, aerobics, dancing. Supports heart and lung health.

**Strength/Resistance Training**
- Weightlifting, resistance bands, bodyweight exercises (push-ups, squats, lunges, planks), gym machines. Builds muscle and bone density.

**Flexibility & Mobility**
- Yoga, Pilates, stretching routines. Increases range of motion and prevents injury.

**Balance & Core Stability**
- Tai chi, Pilates, stability ball exercises, single-leg stands, planks. Improves coordination and prevents falls.

**Lifestyle & Functional Activity**
- Climbing stairs, gardening, housework, carrying groceries, active commuting.

**General Recommendations**
- Adults: At least 150 minutes moderate aerobic activity/week OR 75 minutes vigorous activity.
- Strength train all major muscle groups 2+ times/week.
- Stretch 2–3 times/week.
- Include balance/core work, especially for older adults.

**Special Considerations**
- Outdoor activities help with vitamin D.
- Modify intensity for anemia, cardiovascular, or joint issues.
- Always warm up and cool down.

*Agent: Select the most appropriate exercise types and advice for the patient's condition, based on this reference list!*
""".strip()