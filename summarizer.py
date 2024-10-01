import time
import anthropic

# Replace with your actual API key
CLAUDE_API_KEY = "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"

# Initialize the Anthropic client
client = anthropic.Client(api_key=CLAUDE_API_KEY)

# Simple rate limiting
last_request_time = 0
MIN_REQUEST_INTERVAL = 1  # Minimum time between requests in seconds

def generate_campaign_plan(district, voters, vote_goal, budget, issues, demographics, max_length=300):
    global last_request_time

    # Check rate limiting
    current_time = time.time()
    if current_time - last_request_time < MIN_REQUEST_INTERVAL:
        time.sleep(MIN_REQUEST_INTERVAL - (current_time - last_request_time))

    try:
        prompt = f"""
        You are an expert campaign strategist. Create a detailed campaign plan based on the following input:
        - District: {district}
        - Total voters: {voters}
        - Vote goal: {vote_goal}%
        - Budget: ${budget}
        - Key issues: {issues}
        - District demographics: {demographics}

        The plan should include:
        1. Start with a clear budget breakdown.
        2. Suggest a compelling campaign slogan based on the provided key issues.
        3. A voter outreach strategy based on the district's demographics and key issues.
        4. Recommended media platforms (TV, radio, social media, etc.) and methods (canvassing, direct mail, etc.).
        5. Key messaging points for ads or public appearances.

        Ensure that important elements such as headings, budget breakdown, and voter groups are clearly marked in bold or bullet points. Structure the output for ease of reading.

        Make sure to prioritize Canvassing in the budget breakdown. Always label it 'Media & Outreach' in the voter outreach strategy.
        """

        # Generate the campaign plan using the API
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        plan = response.content[0].text

        # Insert HTML tags or newlines for formatting, and bold key sections
        plan = plan.replace("Budget Breakdown", "<strong>Budget Breakdown</strong>")\
                   .replace("Campaign Slogan", "<strong>Campaign Slogan</strong>")\
                   .replace("Voter Outreach Strategy", "<strong>Voter Outreach Strategy</strong>")\
                   .replace("Recommended Media Platforms and Methods", "<strong>RecommendedMedia Platforms and Methods</strong>")\
                   .replace("Key Messaging Points", "<strong>Key Messaging Points</strong>")\
                   .replace("Focus on these key voter groups", "<strong>Focus on these key voter groups</strong>")\
                   .replace("Methods", "<strong>Methods</strong>")\
                   .replace("Media Strategy", "<strong>Media Strategy</strong>")\
                   .replace("Key Messaging", "<strong>Key Messaging</strong>")\
                   .replace("Media Platforms", "<strong>Media Platforms</strong>")\
                   .replace("Voter Groups", "<strong>Voter Groups</strong>")\
                   .replace("Recommended Media", "<strong>Recommended Media</strong>")\
                   .replace("\n", "<br>")\
                   .replace("\n\n", "<br><br>")  # Basic formatting with line breaks
        last_request_time = time.time()
        return plan
    except Exception as e:
        raise Exception(f"Error in generating campaign plan: {str(e)}")



# Sample test
if __name__ == "__main__":
    district = "Michigan 7th Congressional District"
    voters = 761621
    vote_goal = 52
    budget = 2392329.72
    issues = "Crime, Economy, Healthcare"
    demographics = "White: 81.62%, Black: 6.07%, Latino: 5.66%, Asian: 3.22%"

    print(generate_campaign_plan(district, voters, vote_goal, budget, issues, demographics))
