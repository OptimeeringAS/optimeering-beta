function sortVersions(versions) {
    return versions.sort((a, b) => {
        if (a == "latest") {
            return -1
        }
        if (b == "latest") {
            return 1
        }
        a = parseInt(a.substring(1))
        b = parseInt(b.substring(1))
        if (a > b) {
            return -1
        }
        else {
            return 1
        }
    })
}

async function getVersions(baseURL) {
    const response = await fetch(baseURL + "/versions.json")

    // Anything other than ok indicates the user is not authenticated
    if (response.ok) {
        const versions = await response.json().then(
            (versions) => {
                return sortVersions(versions)
            })
        return versions
    } else {
        return []
    }
}

(function () {
    window.addEventListener("load", function () {
        setTimeout(async function () {
            var href = window.location.href.split("/");
            var baseURL = href.slice(0, -2).join("/");
            var currentVersion = href[href.length - 2]

            const currentVersionDiv = document.getElementById('current-version')
            currentVersionDiv.innerHTML = "Version: " + currentVersion

            const versions = await getVersions(baseURL)
            const versionList = document.getElementById('version-list')
                .appendChild(
                    document.createElement("dl")
                )

            for (version of versions) {
                let dd = document.createElement("dd")

                let a = document.createElement("a")
                if (version == currentVersion) {
                    a.className = "selected-version"
                }
                a.innerHTML = version
                a.href = baseURL + "/" + version + "/index.html"
                dd.appendChild(a)
                versionList.appendChild(dd)

            }
        }, 100);
    });
})();