function replaceBanner(newBannerSrc) {
    const bannerElement = document.getElementById('banner');
    if (bannerElement) {
        bannerElement.src = newBannerSrc;
    }
}

function replaceProjectName(newProjectName) {
    const projectNameElement = document.getElementById('projectName');
    if (projectNameElement) {
        projectNameElement.textContent = `Muk | ${newProjectName}`;
    }
}

// This function loads the template and updates the banner and project name
function loadTopTemplate() {
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
}

document.addEventListener("DOMContentLoaded", function () {
    loadTopTemplate();
});