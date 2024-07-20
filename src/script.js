document.addEventListener('DOMContentLoaded', () => {
    fetch('https://crchttpfunction.azurewebsites.net/api/main?code=YHMOtJ7IRu4pEpRmRknbkjnzfhnxpSHhMmMFbC4lFN8cAzFuKkr2MQ%3D%3D')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('visitor-count').innerText = data.count;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('visitor-count').innerText = 'Error loading count';
        });
});
