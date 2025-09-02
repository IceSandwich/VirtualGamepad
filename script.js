document.querySelectorAll('.button').forEach(button => {
    button.addEventListener('mousedown', () => {
        button.style.backgroundColor = '#999';
        console.log(`${button.id} pressed`);
    });

    button.addEventListener('mouseup', () => {
        button.style.backgroundColor = '#777';
        console.log(`${button.id} released`);
    });
});

document.querySelectorAll('.joystick').forEach(joystick => {
    joystick.addEventListener('mousedown', (e) => {
        const startX = e.clientX;
        const startY = e.clientY;
        const stick = joystick;
        
        const onMouseMove = (e) => {
            const deltaX = e.clientX - startX;
            const deltaY = e.clientY - startY;
            stick.style.transform = `translate(${deltaX}px, ${deltaY}px)`;
        };

        const onMouseUp = () => {
            document.removeEventListener('mousemove', onMouseMove);
            document.removeEventListener('mouseup', onMouseUp);
            stick.style.transform = 'translate(0, 0)';
            console.log(`${joystick.id} released`);
        };

        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp);
    });
});
