document.addEventListener('DOMContentLoaded', function() {
    const sections = document.querySelectorAll('.section, .subsection');  // accordion applies to .section and .subsection

    sections.forEach(section => {
        const header = section.firstElementChild;  // the first after div is the header
        const content = Array.from(section.children).slice(1);  // everything but the first
const wrapper = document.createElement('div');
        wrapper.classList.add('accordion-wrapper');
        section.insertBefore(wrapper, header);
        wrapper.appendChild(header);
        content.forEach(child => wrapper.appendChild(child));
        header.classList.add('accordion-header');  // label
        content.forEach(child => child.classList.add('accordion-content'));  // label basically

        if (section.id === 'default-open') {
            content.forEach(child => {
                child.style.display = 'block';
            });
        } else {
            content.forEach(child => {
                child.style.display = 'none';
            });
        }

        header.addEventListener('click', () => {
            content.forEach(child => {
                if (child.style.display === 'none' || child.style.display === '') {
                    child.style.display = 'block';
                } else {
                    child.style.display = 'none';
                }
            });
        });
    });
});