console.log('Like button script loaded');
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded event fired');
    const likeButtons = document.querySelectorAll('.like-button-large');
    console.log('Found like buttons:', likeButtons.length);
    
    likeButtons.forEach(button => {
        console.log('Setting up click handler for button:', button);
        button.addEventListener('click', async function(e) {
            console.log('Like button clicked');
            if (this.disabled) {
                console.log('Button is disabled');
                return;
            }
            
            const slug = this.dataset.articleSlug;
            console.log('Article slug:', slug);
            const url = `/articles/${slug}/like/`;
            
            try {
                console.log('Sending request to:', url);
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    }
                });
                
                console.log('Response status:', response.status);
                if (response.ok) {
                    const data = await response.json();
                    console.log('Response data:', data);
                    
                    // Update button state
                    if (data.liked) {
                        this.classList.add('liked');
                    } else {
                        this.classList.remove('liked');
                    }
                    
                    // Update likes count
                    const likesCount = this.querySelector('.likes-count');
                    if (likesCount) {
                        likesCount.textContent = data.likes_count;
                    }
                } else {
                    console.error('Server returned error:', response.status);
                }
            } catch (error) {
                console.error('Error toggling like:', error);
            }
        });
    });
});
