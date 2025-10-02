const jsonUrl = "https://raw.githubusercontent.com/LaboratorioSperimentale/DiCCAS/refs/heads/interface/interface/data.json";


async function fetchJSON() {
	// Load the JSON data
    const response = await fetch(jsonUrl);
	const data = await response.json();

	return data;

}

// ON LOAD
document.addEventListener("DOMContentLoaded", () => {
	let data = fetchJSON();
	console.log(data)
});


