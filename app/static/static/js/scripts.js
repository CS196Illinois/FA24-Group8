async function filterResults() {
    const researchArea = document.getElementById('researchArea').value;
    const opportunityTiming = document.getElementById('opportunityTiming').value;
    const location = document.getElementById('location').value;
    const deadlineBefore = document.getElementById('deadlineBefore').value;

    const apiUrl = `/filter?research_area=${researchArea}&opportunity_timing=${opportunityTiming}&location=${location}&deadline_before=${deadlineBefore}`;

    const response = await fetch(apiUrl);
    const results = await response.json();

    const resultsTable = document.getElementById('resultsTable');
    resultsTable.innerHTML = '';
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
