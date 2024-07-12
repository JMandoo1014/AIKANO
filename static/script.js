document.addEventListener('DOMContentLoaded', function () {
    const conversationDiv = document.getElementById('conversation');
    const circle = document.getElementById('circle');
    const aiName = document.querySelector('.ai-name');

    // 펄스 애니메이션
    circle.addEventListener('click', function () {
        conversationDiv.innerHTML = '<p>말씀하세요...</p>';

        fetch('/process_audio', {
            method: 'POST',
        })
        .then(response => response.text())
        .then(data => {
            // 서버에서 응답을 받아와 텍스트로 먼저 표시
            conversationDiv.innerHTML += `<p>${data}</p>`;

            // 음성 파일 재생을 위한 추가 처리
            const audioUrl = `/static/${data}.mp3`; // 서버에서 반환하는 음성 파일 경로
            const audio = new Audio(audioUrl);
            audio.play();

            // 펄스 애니메이션 트리거
            circle.style.animation = 'none'; // 애니메이션 초기화
            void circle.offsetWidth; // 리플로우 강제 실행
            circle.style.animation = 'pulse 2s infinite alternate'; // 펄스 애니메이션 재시작
        })
        .catch(error => {
            console.error('에러 발생:', error);
            conversationDiv.innerHTML += '<p>서버 오류 발생</p>';
        });
    });

    // "AIKANO" 텍스트 애니메이션
    setTimeout(function () {
        aiName.style.opacity = '0.8'; // 초기에 투명도를 설정하여 나타나게 함
        aiName.style.animation = 'fade-in 2s forwards'; // fade-in 애니메이션 적용
    }, 1000); // 1초 뒤에 애니메이션 시작
});
