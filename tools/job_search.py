import requests


def search_jobs(query):

    url = "https://remotive.com/api/remote-jobs"

    response = requests.get(url)

    data = response.json()

    jobs = data["jobs"]

    results = []

    for job in jobs:

        title = job["title"]

        if query.lower() in title.lower():

            results.append({
                "title": title,
                "company": job["company_name"],
                "location": job["candidate_required_location"],
                "url": job["url"]
            })

    return results[:5]
    