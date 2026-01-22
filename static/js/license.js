const viewer = document.getElementById('imageViewer');
    const viewerImage = document.getElementById('viewerImage');
    const closeBtn = viewer.querySelector('.close');

    let scale = 1;
    let isDragging = false;
    let startX, startY, translateX = 0, translateY = 0;

    document.querySelectorAll('.license-block .image img')
        .forEach(img => {
            img.addEventListener('click', () => {
                viewerImage.src = img.src;
                viewer.style.display = 'flex';

                // reset
                scale = 1;
                translateX = 0;
                translateY = 0;
                viewerImage.style.transform = 'scale(1) translate(0, 0)';
            });
        });

    /* Zoom колесом */
    viewer.addEventListener('wheel', (e) => {
        e.preventDefault();
        scale += e.deltaY * -0.001;
        scale = Math.min(Math.max(1, scale), 4); // 1x–4x
        updateTransform();
    });

    /* Drag */
    viewerImage.addEventListener('mousedown', (e) => {
        isDragging = true;
        viewerImage.style.cursor = 'grabbing';
        startX = e.clientX - translateX;
        startY = e.clientY - translateY;
    });

    window.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        translateX = e.clientX - startX;
        translateY = e.clientY - startY;
        updateTransform();
    });

    window.addEventListener('mouseup', () => {
        isDragging = false;
        viewerImage.style.cursor = 'grab';
    });

    function updateTransform() {
        viewerImage.style.transform =
            `translate(${translateX}px, ${translateY}px) scale(${scale})`;
    }

    /* Закрытие */
    closeBtn.addEventListener('click', closeViewer);

    viewer.addEventListener('click', (e) => {
        if (e.target === viewer) closeViewer();
    });

    function closeViewer() {
        viewer.style.display = 'none';
        viewerImage.src = '';
    }