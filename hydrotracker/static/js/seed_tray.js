document.addEventListener('DOMContentLoaded', function() {
    const gridSquares = document.querySelectorAll('.seed-tray-square');

    gridSquares.forEach(square => {
        square.addEventListener('click', function(event) {
            const position = this.dataset.position; // Assume data-position="x-y" is set on each square div
            // Handle the click event, either by marking it for a new plant or selecting it for moving
        });
    });

    // Additional logic to handle dragging and dropping will go here
});
