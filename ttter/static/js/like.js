const getCookie = (name) => {
    if (document.cookie && document.cookie !== '') {
        for (const cookie of document.cookie.split(';')) {
            const [key, value] = cookie.trim().split('=');
            if (key === name) {
                return decodeURIComponent(value);
            }
        }
    }
};
const csrftoken = getCookie('csrftoken');

const LikeAction = async (tweet_id) => {
    console.log(tweet_id);
    const tweet_element =  document.getElementById(tweet_id);
    const url = tweet_element.dataset.url;
    const data = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
    }
    const response = await fetch(url, data);
    const tweet_data = await response.json();
    changeStyle(tweet_data, tweet_element);
}

const changeStyle = (tweet_data, selector) => {
    const count = document.querySelector(`[name="count_${tweet_data.tweet_id}"]`)
    if (tweet_data.is_liked) {
        const unlike_url = `/unlike/${tweet_data.tweet_id}/`
        selector.setAttribute('data-url', unlike_url);
        selector.innerHTML = "いいね解除";
        count.innerHTML = tweet_data.liked_count;
    } else {
        const like_url = `/like/${tweet_data.tweet_id}/`
        selector.setAttribute('data-url', like_url);
        selector.innerHTML = "いいね";
        count.innerHTML = tweet_data.liked_count;
    }
}
