console.log("filterResults function is called");
async function filterResults() {
    // Get selected filter criteria
    const researchArea = document.getElementById('researchArea').value;
    const opportunityTiming = document.getElementById('opportunityTiming').value;
    const location = document.getElementById('location').value;
    const deadlineBefore = document.getElementById('deadlineBefore').value;

    // Build API request URL
    const apiUrl = `/filter?research_area=${researchArea}&opportunity_timing=${opportunityTiming}&location=${location}&deadline_before=${deadlineBefore}`;

    // Send the request to the backend
    const response = await fetch(apiUrl);
    const results = await response.json();

    // Render results into the table
    const resultsTable = document.getElementById('resultsTable');
    resultsTable.innerHTML = ''; // Clear the table
    if (results.length === 0) {
        resultsTable.innerHTML = '<tr><td colspan="6">No opportunities found.</td></tr>';
    } else {
        results.forEach(result => {
            const row = `
                <tr>
                    <td>${result.Topic}</td>
                    <td>${result.Description}</td>
                    <td>${result['Research Area']}</td>
                    <td>${result['Opportunity Timing']}</td>
                    <td>${result['Deadline Date']}</td>
                    <td>${result.Location}</td>
                </tr>
            `;
            resultsTable.innerHTML += row;
        });
    }
}

async function loadOptions() {
    const response = await fetch('/get-options');
    const data = await response.json();

    // Research Area Choices
    const researchAreaSelect = document.getElementById('researchArea');
    researchAreaSelect.innerHTML = '<option value="">-- Select Research Area --</option>';
    data.research_areas.forEach(area => {
        const option = document.createElement('option');
        option.value = area;
        option.textContent = area;
        researchAreaSelect.appendChild(option);
    });

    // Opportunity Timing Choices
    const opportunityTimingSelect = document.getElementById('opportunityTiming');
    opportunityTimingSelect.innerHTML = '<option value="">-- Select Opportunity Timing --</option>';
    data.opportunity_timings.forEach(timing => {
        const option = document.createElement('option');
        option.value = timing;
        option.textContent = timing;
        opportunityTimingSelect.appendChild(option);
    });
}

document.addEventListener('DOMContentLoaded', loadOptions);