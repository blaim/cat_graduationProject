Kakao.init('9bbfbba5ae61bfb9494771bd71ad837b');
console.log(Kakao.isInitialized());

function logintest()
{
    Kakao.Auth.authorize({
        redirectUri: 'http://127.0.0.1:8000/top',
        scope: 'profile_nickname'
    });
}