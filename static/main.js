document.addEventListener("DOMContentLoaded", async function(event) {
	if (window.location.href.indexOf("filter.html") > -1) {
		await filterResults();
	}
});

async function filterResults() {
    // Get user input for filter criteria
    const researchArea = document.getElementById('researchArea').value;
    const opportunityTiming = document.getElementById('opportunityTiming').value;
    const deadlineBefore = document.getElementById('deadlineBefore').value;

    // Build the API request URL
    const apiUrl = `/filter?research_area=${researchArea}&opportunity_timing=${opportunityTiming}&deadline_before=${deadlineBefore}`;

    // Send the request to the backend
    const response = await fetch(apiUrl);
    const results = await response.json();

    // Render results into the table
    const resultsTable = document.getElementById('resultsTable');
    resultsTable.innerHTML = ''; // Clear the table
    results.forEach(result => {
        const row = `
            <tr>
                <td><a href = "${result.DetailURL}">${result.Title}</a></td>
                <td>${result.Description}</td>
                <td>${result['Research Area']}</td>
                <td>${result['Opportunity Timing']}</td>
                <td>${result['Deadline Date']}</td>
            </tr>
        `;
        resultsTable.innerHTML += row;
    });
}

document.addEventListener("DOMContentLoaded", async function(event) {
	if (window.location.href.indexOf("recommendation.html") > -1) {
		await recommendResults();
	}
});

async function recommendResults() {
    // Get user input for filter criteria
    const researchInterest1 = document.getElementById('researchInterest1').value;
    const researchInterest2 = document.getElementById('researchInterest2').value;
    const researchInterest3 = document.getElementById('researchInterest3').value;

    // Build the API request URL
    const apiUrl = `/recommend_filter?researchInterest1=${researchInterest1}&researchInterest2=${researchInterest2}&researchInterest3=${researchInterest3}`;

    // Send the request to the backend
    const response = await fetch(apiUrl);
    const results = await response.json();

    // Render results into the table
    const resultsTable = document.getElementById('resultsRecommendationsTable');
    resultsTable.innerHTML = ''; // Clear the table
    results.forEach(result => {
        const row = `
            <tr>
                <td><a href = "${result.DetailURL}">${result.Title}</a></td>
                <td>${result.Description}</td>
                <td>${result['Research Area']}</td>
                <td>${result['Opportunity Timing']}</td>
                <td>${result['Deadline Date']}</td>
            </tr>
        `;
        resultsTable.innerHTML += row;
    });
}