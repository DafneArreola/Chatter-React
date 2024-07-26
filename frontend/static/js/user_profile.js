document.addEventListener('DOMContentLoaded', () => {
    const ratingSortSelect = document.getElementById('ratingSort');
    const ratingFilterSelect = document.getElementById('ratingFilter');
    const commentSortSelect = document.getElementById('commentSort');
    const commentFilterSelect = document.getElementById('commentFilter');

    function sortList(list, sortBy) {
        const items = Array.from(list.children);
        if (sortBy === 'none') return;

        items.sort((a, b) => {
            const textA = a.querySelector('h4').innerText;
            const textB = b.querySelector('h4').innerText;

            if (sortBy === 'a-z') return textA.localeCompare(textB);
            if (sortBy === 'z-a') return textB.localeCompare(textA);

            return 0;
        });

        items.forEach(item => list.appendChild(item));
    }

    function filterList(list, filterBy) {
        list.querySelectorAll('li').forEach(item => {
            const type = item.getAttribute('data-type');
            const shouldDisplay = (filterBy === 'all' || type === filterBy);

            // Show/Hide the media item and its nested lists
            if (shouldDisplay) {
                item.classList.remove('hidden');
                item.querySelectorAll('ul').forEach(childList => {
                    childList.classList.remove('hidden');
                });
            } else {
                item.classList.add('hidden');
                item.querySelectorAll('ul').forEach(childList => {
                    childList.classList.add('hidden');
                });
            }
        });
    }

    function handleFilterAndSort() {
        const selectedRatingFilter = ratingFilterSelect.value;
        const selectedCommentFilter = commentFilterSelect.value;

        // Apply filtering
        filterList(document.getElementById('ratingsList'), selectedRatingFilter);
        filterList(document.getElementById('commentsList'), selectedCommentFilter);

        // Apply sorting
        sortList(document.getElementById('ratingsList'), ratingSortSelect.value);
        sortList(document.getElementById('commentsList'), commentSortSelect.value);
    }

    ratingSortSelect.addEventListener('change', handleFilterAndSort);
    ratingFilterSelect.addEventListener('change', handleFilterAndSort);
    commentSortSelect.addEventListener('change', handleFilterAndSort);
    commentFilterSelect.addEventListener('change', handleFilterAndSort);
});
