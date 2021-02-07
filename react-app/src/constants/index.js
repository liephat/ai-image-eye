
// hostname in dev environment
export const FLASK_HOST = "http://localhost:5000/";

export function flaskUrl(path) {
    return FLASK_HOST + path;
}
