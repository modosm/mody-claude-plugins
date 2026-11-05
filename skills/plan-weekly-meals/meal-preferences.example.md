# Meal-planning profile

Private inputs for the `plan-weekly-meals` skill. Copy this file to
`~/github/mody-claude-plugins/config/meal-preferences.local.md` (gitignored)
and fill in real values. Never commit the filled-in copy.

## Targets

- Calories: approximately <kcal> kcal/day.
- Protein: <min>-<max> g/day.
- Goal: <e.g. fat loss while keeping muscle>.

## Fixed breakfast

- <item and amount>
- <item and amount>

Until exact product labels are supplied, use this working estimate:

- Breakfast total: <kcal> kcal and <g> g protein.
- One additional whey serving: <kcal> kcal and <g> g protein.

Label these as estimates because they don't come from the menu PDF.

## Dietary constraints

- Exclude <ingredient> (<Hungarian menu names>), including sides, purées and mixed dishes. <Related ingredient> remains allowed.
- Avoid <ingredient> as a standalone item or primary ingredient. Permit <related items>.
- Minimize <ingredient>.

## Extra whey

<When to add a serving, e.g. only when daily protein is below the minimum. Never add whey just to make up missing calories.>

## Selection priorities

Apply these in order:

1. Dietary safety and explicit exclusions.
2. Correct menu day and weekend sourcing.
3. At least <min> g daily protein where practical.
4. Reasonable proximity to <kcal> kcal.
5. Variety across proteins, cuisines, and meal types.
6. Minimal reliance on extra whey.
