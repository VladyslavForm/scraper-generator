# Task 04: LLM Integration for Intelligent Analysis

## Goal
Integrate with OpenRouter API to use LLM (Claude) for analyzing HTML structure and validating/improving the automatically detected CSS selectors.

## Why LLM Integration?

Automatic detection works well for typical sites, but LLM adds:
- Better understanding of unusual HTML structures
- Validation that selectors actually make sense
- Ability to refine selectors that don't work
- Confidence scoring for detection results

## Implementation Tasks

### 1. Implement `__init__()` Method

Initialize the LLM client:
- Load OPENROUTER_API_KEY from environment (use dotenv)
- Load OPENROUTER_MODEL from environment (default to claude-3.5-sonnet)
- Raise clear error if API key is missing
- Create OpenAI client instance with:
  - base_url = "https://openrouter.ai/api/v1"
  - api_key from environment
- Store client as instance variable

### 2. Implement `analyze_html_structure()` Method

**Method signature:** 
`analyze_html_structure(homepage_html, article_htmls, detected_selectors)`

**Purpose:** Send HTML samples to LLM for analysis

**What to do:**
1. Prepare a prompt that includes:
   - Truncated homepage HTML (first ~3000 chars)
   - Truncated sample article HTML (first ~3000 chars)
   - The selectors already detected automatically
   
2. Create a system message that explains:
   - You're analyzing website structure
   - Goal is to find CSS selectors for scraping
   - Need selectors for: article links, title, content
   - Selectors will be used with BeautifulSoup's `.select()` method

3. Create a user prompt that asks LLM to:
   - Validate the pre-detected selectors
   - Suggest improvements if needed
   - Respond ONLY with JSON in this format:
     ```json
     {
       "selectors": {
         "article_links": "CSS selector",
         "title": "CSS selector",
         "content": "CSS selector"
       },
       "confidence": "high/medium/low",
       "notes": "observations about site structure",
       "potential_issues": ["list of concerns if any"]
     }
     ```

4. Make API call with:
   - model: from config
   - temperature: 0.3 (for consistency)
   - messages: system + user

5. Parse JSON response:
   - Try json.loads() on response content
   - If that fails, use regex to extract JSON from markdown code blocks
   - If parsing fails completely, return error dict

6. Return the parsed result

**Error handling:**
- Catch API errors (network, rate limits, auth)
- Return dict with 'error' key on failure
- Never crash - always return something useful

### 3. Implement `validate_selectors()` Method

**Method signature:** `validate_selectors(test_html, selectors)`

**Purpose:** Test if selectors actually work on HTML

**What to do:**
1. Parse test_html with BeautifulSoup
2. For each selector in the selectors dict:
   - Try `soup.select(selector)`
   - Check if any elements were found
   - Record True/False for each selector
3. Return dict mapping selector names to boolean results

Example return:
```python
{
    'article_links': True,   # Found elements
    'title': True,           # Found elements
    'content': False         # Found nothing
}
```

**Error handling:**
- Catch selector syntax errors (invalid CSS)
- Return False for selectors that cause errors

### 4. Implement `refine_selectors_with_feedback()` Method

**Method signature:** 
`refine_selectors_with_feedback(selectors, validation_results, html_sample)`

**Purpose:** Ask LLM to fix selectors that failed validation

**What to do:**
1. Check which selectors failed validation
2. If all selectors passed, return selectors unchanged
3. If some failed, create a prompt that:
   - Shows the failed selectors
   - Includes HTML sample for context
   - Asks LLM to provide corrected selectors
   - Requests JSON response with fixed selectors
4. Make API call
5. Parse response (similar to analyze_html_structure)
6. Update original selectors dict with fixed ones
7. Return updated selectors

**Prompt structure:**
- Explain which selectors failed
- Show the HTML they need to work on
- Ask for corrections in JSON format
- Request explanation of what was wrong

### 5. Create `SelectorEnhancer` Class (in selector_enhancer.py)

This class combines automatic detection with LLM enhancement:

**In `__init__`:**
- Take base_url parameter
- Create HTMLAnalyzer instance
- Create SelectorDetector instance
- Create LLMClient instance

**In `get_enhanced_selectors()` method:**
Do complete analysis flow:
1. Use HTMLAnalyzer to analyze the site
2. Get homepage soup and article soups
3. Use SelectorDetector to get automatic selectors
4. Send to LLM for enhancement via analyze_html_structure
5. If LLM fails, fall back to automatic selectors
6. Validate the final selectors using first article
7. If validation fails, refine with LLM feedback
8. Return dictionary with:
   - `selectors`: final CSS selectors
   - `method`: 'automatic', 'llm_enhanced', or 'llm_refined'
   - `confidence`: from LLM or 'medium' for automatic
   - `notes`: any important observations
   - `article_urls`: list of all found article URLs

Add informative print statements showing progress through each step.

## Testing Strategy

Create `test_llm.py` that:
1. Starts local server for a test site
2. Creates SelectorEnhancer
3. Calls `get_enhanced_selectors()`
4. Prints:
   - Method used (automatic vs LLM)
   - Confidence level
   - Final selectors
   - Any notes from LLM
   - Number of articles found
5. Validates selectors actually work by trying them on real HTML

## Expected Behavior

For simple sites (like newsroom-hub):
- Automatic detection should work
- LLM validates and confirms
- High confidence

For complex sites:
- Automatic detection might struggle
- LLM provides improvements
- Medium confidence initially
- Refinement step might be needed

## Cost Optimization

To minimize API costs during development:
- Truncate HTML samples (3000 chars is enough)
- Use temperature 0.3 (more deterministic, fewer retries)
- Cache results during testing (optional enhancement)
- Consider using cheaper model for testing (claude-3-haiku)

## Common Challenges

**Challenge**: LLM returns text instead of JSON
**Solution**: Use regex to extract JSON from markdown code blocks (```json ... ```)

**Challenge**: API rate limits
**Solution**: Add retry logic with exponential backoff (or just fail gracefully)

**Challenge**: API key not set
**Solution**: Check in __init__ and give clear error message with setup instructions

**Challenge**: Selectors work in LLM's analysis but not in practice
**Solution**: Always validate with real HTML after getting LLM response

## Prompt Engineering Tips

Make prompts effective:
- Be specific about JSON format requirement
- Show example of desired output structure
- Emphasize that selectors are for BeautifulSoup, not JavaScript
- Provide enough HTML context (but not too much)
- Use clear, structured formatting

## Success Criteria

✅ LLMClient connects to OpenRouter successfully
✅ Can send HTML to LLM and get JSON response
✅ JSON parsing handles various response formats
✅ Validation correctly tests selectors
✅ Refinement improves failed selectors
✅ SelectorEnhancer combines automatic + LLM smoothly
✅ Falls back gracefully if LLM fails
✅ Works end-to-end for at least one test site

## Next Step
Once LLM integration works, proceed to `05-SCRAPER-GENERATOR.md` to generate executable Python code.