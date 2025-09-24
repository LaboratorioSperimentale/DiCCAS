const jsonUrl = 'https://raw.githubusercontent.com/UniDive/corpus-annotation-tools/refs/heads/main/data/latest_export.json';


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


