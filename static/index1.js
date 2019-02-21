 document.addEventListener('DOMContentLoaded', () => {

                // Start by loading first page.
                load_page('home');

                // Set links up to load new pages.
                document.querySelectorAll('.nav-link').forEach(link => {
                    link.onclick = () => {
                        const page = link.dataset.page;
                        load_page(page);
                        return false;
                    };
                });
            });

            // Update text on popping state.
            window.onpopstate = e => {
                const data = e.state;
                document.title = data.title;
                document.querySelector('#body').innerHTML = data.text;
            };

            // Renders contents of new page in main view.
            function load_page(name) {
                const request = new XMLHttpRequest();
                request.open('GET', `/${name}`);
                request.onload = () => {
                    const response = JSON.parse(request.responseText);
                    document.querySelector('#body').innerHTML = response;

                    // Push state to URL.
                    document.title = name;
                    history.pushState({'title': name, 'text': response}, name, name);
                };
                request.send();
            }
