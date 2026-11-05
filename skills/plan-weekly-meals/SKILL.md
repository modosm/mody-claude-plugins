---
name: plan-weekly-meals
description: Plan Máté's weekly meal orders from an attached PDF menu, extracting dish calories and protein, applying his dietary profile, selecting diverse weekday and weekend meals, calculating daily totals and target percentages, and assessing whether the plan supports his goal. Use for weekly menu PDFs, meal-order planning, dish replacements, menu recalculation, or requests to update a previously proposed weekly meal plan.
---

# Plan Weekly Meals

Create a seven-day lunch-and-dinner plan from the supplied menu. Optimize for adherence, protein intake, variety, and the calorie target.

## Load preferences

Read `~/github/mody-claude-plugins/config/meal-preferences.local.md` before choosing dishes or calculating totals. It holds the calorie and protein targets, the goal, breakfast and whey values, exclusions, and selection priorities. It is gitignored, so it only exists on Máté's machines. If it is missing, stop and say so, pointing at `meal-preferences.example.md` next to this file as the template; do not plan from guessed targets or exclusions. Let explicit instructions in the current request override it.

## Inspect the menu

1. Read the attached PDF directly. Use PDF text extraction and render relevant pages when layout, serving sizes, or nutrition values are ambiguous.
2. Identify the weekday represented by each menu section.
3. For each viable dish, capture the exact Hungarian name, calories and protein for the selected serving, relevant ingredients, and available serving sizes.
4. Use nutrition values printed in the PDF. Do not silently substitute database estimates.
5. When several nutrition pairs are printed, infer which pair belongs to each advertised portion from the page layout and state which portion was selected. If the mapping remains ambiguous, ask before finalizing.

## Filter and select

1. Exclude every dish containing an ingredient the profile excludes. Check the full ingredient list, including sides and purées, not just the dish name. Apply each exclusion exactly as written: do not widen it to related ingredients the profile allows.
2. Treat ingredients the profile says to avoid or minimize as soft limits. Use such a meal only when necessary and disclose it.
3. Choose lunch and dinner only from that day's menu Monday through Friday.
4. Choose all Saturday and Sunday meals from Friday's menu.
5. Keep weekend meals distinct from each other. Prefer four different weekend dishes and avoid repeating Friday's own choices when enough suitable options exist.
6. Prefer high-protein meals, but balance the week for variety and calories. Do not choose the same main meal repeatedly merely to maximize protein.

## Calculate totals

1. Apply the breakfast and whey values from the profile, unless current product-label values are supplied.
2. Add extra whey only as described in the profile or the current request.
3. Use `scripts/calculate_plan.py` to calculate and verify total calories, total protein, and percentages against the profile's calorie target and protein minimum and maximum. Input is one JSON file: `{"targets": {"calories", "protein_min", "protein_max", "whey_kcal", "whey_protein"}, "days": [7 × {"day", "breakfast", "lunch", "dinner", "extra_whey_servings"}]}`, where each meal is `{"kcal", "protein"}`.
4. Preserve at least one decimal place for protein and percentages. Use whole calories unless the source requires decimals.
5. Never claim the plan is near the calorie target when the weekly average or several days are materially below it.

## Present the result

Use this exact column order:

`Day | Breakfast | Lunch | Dinner | Extra Whey | Calories | Protein | kcal % | Protein % (<min>g) | Protein % (<max>g)`

Fill `<min>` and `<max>` with the profile's protein range. Include dish calories and protein beside each lunch and dinner name. Keep dish names in Hungarian even when the surrounding response is English.

After the table, report the highest- and lowest-protein days, weekly averages, whether every day reaches the protein minimum, whether calories are genuinely close to the target, and a blunt assessment of whether the plan suits the profile's goal.

Mention assumptions about breakfast nutrition or portion mapping. If calories are too low but protein is already sufficient, recommend ordinary food, especially carbohydrates or fats, instead of automatically adding more whey.

## Handle revisions

When asked to replace a dish, retain every unaffected selection, choose a compliant replacement from the correct day's menu, and recalculate the entire affected day. If a Friday dish used on the weekend changes, check weekend diversity again.
