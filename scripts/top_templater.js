document.addEventListener('DOMContentLoaded', () => {
    // Function to replace the banner image
    function replaceBanner(newBannerSrc) {
        document.getElementById('banner').src = newBannerSrc;
    }

    // Function to replace the project name
    function replaceProjectName(newProjectName) {
        document.getElementById('projectName').textContent = `Muk | ${newProjectName}`;
    }

    // Load the top template
    fetch('top_template.html')
        .then(response => response.text())
        .then(data => {
            const topPlaceholder = document.getElementById('top-placeholder');
            topPlaceholder.innerHTML = data;

            // Get the new banner source and project name from data attributes
            const newBannerSrc = topPlaceholder.getAttribute('data-banner-src');
            const newProjectName = topPlaceholder.getAttribute('data-project-name');

            // Replace the banner and project name if specified
            if (newBannerSrc) {
                replaceBanner(newBannerSrc);
            }
            if (newProjectName) {
                replaceProjectName(newProjectName);
            }
        })
        .catch(error => console.error('Error loading top template:', error));
});