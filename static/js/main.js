document.addEventListener('DOMContentLoaded', () => {
    const summarizeBtn = document.getElementById('summarizeBtn');

    if (summarizeBtn) {
        summarizeBtn.addEventListener('click', async () => {
            const abstractText = document.getElementById('abstractText').innerText;
            const aiSection = document.getElementById('aiSection');
            const loader = document.getElementById('loader');
            const aiContent = document.getElementById('aiContent');
            const shortSummary = document.getElementById('shortSummary');
            const bulletPoints = document.getElementById('bulletPoints');

            aiSection.style.display = 'block';
            loader.style.display = 'block';
            aiContent.style.display = 'none';

            try {
                const response = await fetch('/summarize', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ text: abstractText })
                });

                const data = await response.json();

                if (data.error) {
                    alert('Error: ' + data.error);
                    return;
                }

                shortSummary.innerText = data.summary;
                bulletPoints.innerHTML = '';
                data.bullets.forEach(bullet => {
                    const li = document.createElement('li');
                    li.innerText = bullet;
                    bulletPoints.appendChild(li);
                });

                loader.style.display = 'none';
                aiContent.style.display = 'block';

            } catch (err) {
                console.error(err);
                alert('Failed to generate summary');
                loader.style.display = 'none';
            }
        });
    }

    // Handle all bookmark buttons (detail page and search results)
    document.body.addEventListener('click', async (e) => {
        if (e.target.classList.contains('bookmark-btn')) {
            const btn = e.target;
            const paperData = {
                paper_id: btn.getAttribute('data-paper-id'),
                title: btn.getAttribute('data-title'),
                authors: btn.getAttribute('data-authors'),
                published: btn.getAttribute('data-published'),
                summary: btn.getAttribute('data-summary'),
                pdf_link: btn.getAttribute('data-pdf-link'),
                source: btn.getAttribute('data-source'),
                url: btn.getAttribute('data-url')
            };

            try {
                const response = await fetch('/bookmark/add', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(paperData)
                });

                const data = await response.json();

                if (response.ok) {
                    // Update UI to show bookmarked state
                    btn.classList.add('bookmarked');
                    if (btn.innerText !== '★') {
                        btn.innerText = 'Bookmarked';
                        btn.disabled = true;
                    }
                    alert(data.message);
                } else {
                    if (data.message === 'Already bookmarked') {
                        btn.classList.add('bookmarked');
                        alert('Already in your bookmarks');
                    } else {
                        alert('Error: ' + (data.error || 'Failed to bookmark'));
                    }
                }
            } catch (err) {
                console.error(err);
                alert('Failed to add bookmark');
            }
        }
    });
});
