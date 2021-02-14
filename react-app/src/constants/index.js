
// hostname in dev environment
function getFlaskHost() {
    let host = process.env.REACT_APP_FLASK_HOST;
    if (host !== undefined) {
        return host;
    }
    return window.location.origin + '/';
}

export function flaskUrl(path) {
    return getFlaskHost() + path;
}
