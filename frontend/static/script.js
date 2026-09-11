const API_BASE_URL = "http://127.0.0.1:8000";


let currentAnalysis = null;
let uploadedResume = null;


/* =========================================================
   DOM HELPERS
========================================================= */

function getElement(id) {
    return document.getElementById(id);
}


function parseSkillList(value) {

    if (!value) {
        return [];
    }

    if (Array.isArray(value)) {
        return value;
    }

    if (typeof value !== "string") {
        return [];
    }

    try {

        const parsed = JSON.parse(value);

        if (Array.isArray(parsed)) {
            return parsed;
        }

    } catch (error) {
        // Continue with text parsing.
    }

    return value
        .split(",")
        .map(item => item.trim())
        .filter(Boolean);
}


function parseTextList(value) {

    if (!value) {
        return [];
    }

    if (Array.isArray(value)) {
        return value;
    }

    if (typeof value !== "string") {
        return [];
    }

    try {

        const parsed = JSON.parse(value);

        if (Array.isArray(parsed)) {
            return parsed;
        }

    } catch (error) {
        // Continue with line parsing.
    }

    return value
        .split(/\r?\n/)
        .map(item =>
            item
                .replace(/^[-•*]\s*/, "")
                .trim()
        )
        .filter(Boolean);
}


function escapeHtml(value) {

    if (value === null || value === undefined) {
        return "";
    }

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


/* =========================================================
   STATUS
========================================================= */

function showStatus(message, type = "") {

    const status = getElement("statusMessage");

    if (!status) {
        return;
    }

    status.textContent = message;

    status.className = "status-message";

    if (type) {
        status.classList.add(type);
    }
}


/* =========================================================
   SKILLS
========================================================= */

function displaySkills(
    containerId,
    skills,
    className
) {

    const container = getElement(containerId);

    if (!container) {
        return;
    }

    container.innerHTML = "";

    const skillList = parseSkillList(skills);

    if (skillList.length === 0) {

        container.innerHTML = `
            <span class="empty-message">
                No skills found.
            </span>
        `;

        return;
    }

    skillList.forEach(skill => {

        const tag = document.createElement("span");

        tag.className =
            `skill-tag ${className}`;

        tag.textContent = skill;

        container.appendChild(tag);

    });
}


/* =========================================================
   TEXT LISTS
========================================================= */

function displayTextList(
    containerId,
    items,
    className
) {

    const container = getElement(containerId);

    if (!container) {
        return;
    }

    container.innerHTML = "";

    const list = parseTextList(items);

    if (list.length === 0) {

        container.innerHTML = `
            <div class="empty-message">
                Nothing to display.
            </div>
        `;

        return;
    }

    list.forEach(item => {

        const element = document.createElement("div");

        element.className = className;

        element.textContent = item;

        container.appendChild(element);

    });
}


/* =========================================================
   SCORE HELPERS
========================================================= */

function normalizeScore(value) {

    const number = Number(value);

    if (Number.isNaN(number)) {
        return 0;
    }

    return Math.max(
        0,
        Math.min(
            100,
            number
        )
    );
}


function getScoreColor(score) {

    if (score >= 80) {
        return "#16a34a";
    }

    if (score >= 60) {
        return "#d97706";
    }

    return "#dc2626";
}


function updateScore(
    elementId,
    value
) {

    const element = getElement(elementId);

    if (!element) {
        return;
    }

    const score = normalizeScore(value);

    element.textContent =
        `${Math.round(score)}%`;

    element.style.color =
        getScoreColor(score);

    animateScore(
        element,
        score
    );
}


function animateScore(
    element,
    targetScore
) {

    const duration = 700;

    const startTime = performance.now();

    function update(currentTime) {

        const elapsed =
            currentTime - startTime;

        const progress =
            Math.min(
                elapsed / duration,
                1
            );

        const eased =
            1 -
            Math.pow(
                1 - progress,
                3
            );

        const current =
            targetScore * eased;

        element.textContent =
            `${Math.round(current)}%`;

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}


/* =========================================================
   SCORE CARD VISUALS
========================================================= */

function addScoreVisuals() {

    const scoreCards =
        document.querySelectorAll(
            ".score-card"
        );

    scoreCards.forEach(card => {

        if (
            card.querySelector(
                ".score-progress"
            )
        ) {
            return;
        }

        const progress =
            document.createElement("div");

        progress.className =
            "score-progress";

        progress.innerHTML = `
            <div class="score-progress-ring">
                <div class="score-progress-inner"></div>
            </div>
        `;

        card.appendChild(progress);

    });
}


function updateScoreVisual(
    scoreElementId,
    score
) {

    const scoreElement =
        getElement(scoreElementId);

    if (!scoreElement) {
        return;
    }

    const card =
        scoreElement.closest(
            ".score-card"
        );

    if (!card) {
        return;
    }

    const ring =
        card.querySelector(
            ".score-progress-ring"
        );

    if (!ring) {
        return;
    }

    const normalized =
        normalizeScore(score);

    const color =
        getScoreColor(normalized);

    ring.style.setProperty(
        "--score",
        `${normalized * 3.6}deg`
    );

    ring.style.setProperty(
        "--score-color",
        color
    );

    ring.style.background =
        `conic-gradient(
            ${color}
            ${normalized * 3.6}deg,
            #e5e7eb
            ${normalized * 3.6}deg
        )`;

    ring.classList.add(
        "score-ring-visible"
    );
}


/* =========================================================
   UPLOAD RESUME
========================================================= */

async function uploadResume() {

    const fileInput =
        getElement("resumeFile");

    if (!fileInput) {
        return null;
    }

    const file =
        fileInput.files[0];

    if (!file) {

        showStatus(
            "Please select a resume first.",
            "error"
        );

        return null;
    }

    const allowedExtensions = [
        ".pdf",
        ".docx"
    ];

    const fileName =
        file.name.toLowerCase();

    const validExtension =
        allowedExtensions.some(
            extension =>
                fileName.endsWith(
                    extension
                )
        );

    if (!validExtension) {

        showStatus(
            "Only PDF and DOCX files are allowed.",
            "error"
        );

        return null;
    }


    const formData =
        new FormData();

    formData.append(
        "file",
        file
    );


    try {

        showStatus(
            "Uploading resume..."
        );

        const response =
            await fetch(
                `${API_BASE_URL}/resume/upload`,
                {
                    method: "POST",
                    body: formData
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Resume upload failed."
            );
        }


        uploadedResume = data;


        const selectedFile =
            getElement(
                "selectedFileName"
            );


        if (selectedFile) {

            selectedFile.textContent =
                `Selected: ${data.filename}`;

        }


        showStatus(
            "Resume uploaded successfully.",
            "success"
        );


        return data;

    } catch (error) {

        console.error(
            "Upload error:",
            error
        );


        showStatus(
            error.message ||
            "Could not upload resume.",
            "error"
        );


        return null;
    }
}


/* =========================================================
   ANALYZE RESUME
========================================================= */

async function analyzeResume() {

    const fileInput =
        getElement("resumeFile");

    const jobDescriptionInput =
        getElement("jobDescription");


    if (!fileInput ||
        !fileInput.files[0]) {

        showStatus(
            "Please upload your resume first.",
            "error"
        );

        return;
    }


    const jobDescription =
        jobDescriptionInput
            ? jobDescriptionInput.value.trim()
            : "";


    if (!jobDescription) {

        showStatus(
            "Please enter a job description.",
            "error"
        );

        return;
    }


    const analyzeButton =
        getElement(
            "analyzeButton"
        );


    if (analyzeButton) {

        analyzeButton.disabled =
            true;

        analyzeButton.innerHTML = `
            <span>
                Analyzing...
            </span>
            <span class="button-arrow">
                •••
            </span>
        `;
    }


    try {

        let uploadData =
            uploadedResume;


        if (!uploadData) {

            uploadData =
                await uploadResume();

            if (!uploadData) {
                return;
            }
        }


        showStatus(
            "Analyzing your resume..."
        );


        const response =
            await fetch(
                `${API_BASE_URL}/analysis/`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        resume_filename:
                            uploadData.filename,

                        job_description:
                            jobDescription
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Analysis failed."
            );
        }


        currentAnalysis =
            data;


        displayAnalysis(
            data
        );


        showStatus(
            "Analysis completed successfully.",
            "success"
        );


        const analysisSection =
            getElement(
                "analysisSection"
            );


        if (analysisSection) {

            analysisSection.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        }


        await loadHistory();

    } catch (error) {

        console.error(
            "Analysis error:",
            error
        );


        showStatus(
            error.message ||
            "Something went wrong while analyzing the resume.",
            "error"
        );

    } finally {

        if (analyzeButton) {

            analyzeButton.disabled =
                false;

            analyzeButton.innerHTML = `
                <span>
                    Analyze Resume
                </span>

                <span class="button-arrow">
                    →
                </span>
            `;
        }
    }
}


/* =========================================================
   DISPLAY ANALYSIS
========================================================= */

function displayAnalysis(
    analysis
) {

    if (!analysis) {
        return;
    }


    const analysisSection =
        getElement(
            "analysisSection"
        );


    if (analysisSection) {

        analysisSection.style.display =
            "block";
    }


    addScoreVisuals();


    /* -------------------------
       Scores
    ------------------------- */

    updateScore(
        "matchScore",
        analysis.match_score
    );

    updateScore(
        "technicalScore",
        analysis.technical_score
    );

    updateScore(
        "softSkillScore",
        analysis.soft_skill_score
    );

    updateScore(
        "qualityScore",
        analysis.quality_score
    );


    setTimeout(() => {

        updateScoreVisual(
            "matchScore",
            analysis.match_score
        );

        updateScoreVisual(
            "technicalScore",
            analysis.technical_score
        );

        updateScoreVisual(
            "softSkillScore",
            analysis.soft_skill_score
        );

        updateScoreVisual(
            "qualityScore",
            analysis.quality_score
        );

    }, 50);


    /* -------------------------
       Job Skill Priorities
    ------------------------- */

    const requiredSkills =
        parseSkillList(
            analysis.required_skills
        );


    const preferredSkills =
        parseSkillList(
            analysis.preferred_skills
        );


    const generalSkills =
        parseSkillList(
            analysis.general_skills
        );


    displaySkills(
        "requiredSkills",
        requiredSkills,
        "required-skill"
    );


    displaySkills(
        "preferredSkills",
        preferredSkills,
        "preferred-skill"
    );


    displaySkills(
        "generalSkills",
        generalSkills,
        "general-skill"
    );


    /* -------------------------
       Matching / Missing
    ------------------------- */

    const matchingSkills =
        parseSkillList(
            analysis.matching_skills
        );


    const missingSkills =
        parseSkillList(
            analysis.missing_skills
        );


    displaySkills(
        "matchingSkills",
        matchingSkills,
        "matching-skill"
    );


    displaySkills(
        "missingSkills",
        missingSkills,
        "missing-skill"
    );


    /* -------------------------
       Missing Skill Priorities
    ------------------------- */

    const missingSet =
        new Set(
            missingSkills.map(
                skill =>
                    skill.toLowerCase()
            )
        );


    const highPriorityMissing =
        requiredSkills.filter(
            skill =>
                missingSet.has(
                    skill.toLowerCase()
                )
        );


    const mediumPriorityMissing =
        preferredSkills.filter(
            skill =>
                missingSet.has(
                    skill.toLowerCase()
                )
        );


    const lowPriorityMissing =
        generalSkills.filter(
            skill =>
                missingSet.has(
                    skill.toLowerCase()
                )
        );


    displaySkills(
        "highPriorityMissingSkills",
        highPriorityMissing,
        "missing-skill"
    );


    displaySkills(
        "mediumPriorityMissingSkills",
        mediumPriorityMissing,
        "missing-skill"
    );


    displaySkills(
        "lowPriorityMissingSkills",
        lowPriorityMissing,
        "missing-skill"
    );


    /* -------------------------
       Suggestions
    ------------------------- */

    displayTextList(
        "suggestions",
        analysis.suggestions,
        "suggestion-item"
    );


    /* -------------------------
       AI Recommendations
    ------------------------- */

    displayRecommendations(
        analysis.recommendations ||
        analysis.ai_recommendations ||
        []
    );


    /* -------------------------
       Quality
    ------------------------- */

    displayQuality(
        "qualityStrengths",
        analysis.quality_strengths,
        "quality-strength"
    );


    displayQuality(
        "qualityWarnings",
        analysis.quality_warnings,
        "quality-warning"
    );


    /* -------------------------
       Statistics
    ------------------------- */

    setText(
        "wordCount",
        analysis.word_count ?? 0
    );


    setText(
        "actionVerbCount",
        analysis.action_verb_count ?? 0
    );


    setText(
        "quantifiableAchievementCount",
        analysis.quantifiable_achievement_count ?? 0
    );


    /* -------------------------
       Report
    ------------------------- */

    setText(
        "resumeFilename",
        analysis.resume_filename || "-"
    );


    setText(
        "analysisId",
        analysis.id ?? "-"
    );


    /* -------------------------
       Animate cards
    ------------------------- */

    animateResultCards();
}


/* =========================================================
   QUALITY
========================================================= */

function displayQuality(
    containerId,
    values,
    className
) {

    const container =
        getElement(containerId);

    if (!container) {
        return;
    }

    container.innerHTML = "";

    const list =
        parseTextList(values);


    if (list.length === 0) {

        container.innerHTML = `
            <div class="empty-message">
                No information available.
            </div>
        `;

        return;
    }


    list.forEach(item => {

        const element =
            document.createElement("div");

        element.className =
            `quality-item ${className}`;

        element.textContent =
            item;

        container.appendChild(
            element
        );

    });
}


/* =========================================================
   RECOMMENDATIONS
========================================================= */

function displayRecommendations(
    recommendations
) {

    const container =
        getElement(
            "aiRecommendations"
        );

    if (!container) {
        return;
    }

    container.innerHTML = "";


    const list =
        parseTextList(
            recommendations
        );


    if (list.length === 0) {

        container.innerHTML = `
            <div class="empty-message">
                AI recommendations will appear here
                when additional recommendation data is available.
            </div>
        `;

        return;
    }


    list.forEach(item => {

        const element =
            document.createElement("div");

        element.className =
            "recommendation-item";

        element.textContent =
            item;

        container.appendChild(
            element
        );

    });
}


/* =========================================================
   SET TEXT
========================================================= */

function setText(
    id,
    value
) {

    const element =
        getElement(id);

    if (!element) {
        return;
    }

    element.textContent =
        value;
}


/* =========================================================
   RESULT ANIMATION
========================================================= */

function animateResultCards() {

    const elements =
        document.querySelectorAll(
            ".score-card, .content-card, .report-card"
        );


    elements.forEach(
        (element, index) => {

            element.style.opacity =
                "0";

            element.style.transform =
                "translateY(15px)";


            setTimeout(() => {

                element.style.transition =
                    "opacity 0.45s ease, transform 0.45s ease";

                element.style.opacity =
                    "1";

                element.style.transform =
                    "translateY(0)";

            }, index * 35);

        }
    );
}


/* =========================================================
   DOWNLOAD REPORT
========================================================= */

function downloadReport() {

    if (!currentAnalysis) {

        showStatus(
            "Please analyze a resume first.",
            "error"
        );

        return;
    }


    const analysis =
        currentAnalysis;


    const matchingSkills =
        parseSkillList(
            analysis.matching_skills
        );


    const missingSkills =
        parseSkillList(
            analysis.missing_skills
        );


    const requiredSkills =
        parseSkillList(
            analysis.required_skills
        );


    const preferredSkills =
        parseSkillList(
            analysis.preferred_skills
        );


    const generalSkills =
        parseSkillList(
            analysis.general_skills
        );


    const missingSet =
        new Set(
            missingSkills.map(
                skill =>
                    skill.toLowerCase()
            )
        );


    const highMissing =
        requiredSkills.filter(
            skill =>
                missingSet.has(
                    skill.toLowerCase()
                )
        );


    const mediumMissing =
        preferredSkills.filter(
            skill =>
                missingSet.has(
                    skill.toLowerCase()
                )
        );


    const lowMissing =
        generalSkills.filter(
            skill =>
                missingSet.has(
                    skill.toLowerCase()
                )
        );


    const suggestions =
        parseTextList(
            analysis.suggestions
        );


    const strengths =
        parseTextList(
            analysis.quality_strengths
        );


    const warnings =
        parseTextList(
            analysis.quality_warnings
        );


    let report = "";


    report +=
        "AI RESUME ANALYZER\n";

    report +=
        "============================\n\n";


    report +=
        `Resume: ${analysis.resume_filename || "-"}\n`;

    report +=
        `Analysis ID: ${analysis.id || "-"}\n`;

    report +=
        `Date: ${analysis.created_at || new Date().toLocaleString()}\n\n`;


    report +=
        "SCORES\n";

    report +=
        "----------------------------\n";

    report +=
        `Overall Match: ${normalizeScore(analysis.match_score).toFixed(1)}%\n`;

    report +=
        `Technical Score: ${normalizeScore(analysis.technical_score).toFixed(1)}%\n`;

    report +=
        `Soft Skill Score: ${normalizeScore(analysis.soft_skill_score).toFixed(1)}%\n`;

    report +=
        `Resume Quality: ${normalizeScore(analysis.quality_score).toFixed(1)}%\n\n`;


    report +=
        "REQUIRED SKILLS\n";

    report +=
        "----------------------------\n";

    report +=
        requiredSkills.join(", ") ||
        "None";

    report +=
        "\n\n";


    report +=
        "PREFERRED SKILLS\n";

    report +=
        "----------------------------\n";

    report +=
        preferredSkills.join(", ") ||
        "None";

    report +=
        "\n\n";


    report +=
        "GENERAL SKILLS\n";

    report +=
        "----------------------------\n";

    report +=
        generalSkills.join(", ") ||
        "None";

    report +=
        "\n\n";


    report +=
        "MATCHING SKILLS\n";

    report +=
        "----------------------------\n";

    report +=
        matchingSkills.join(", ") ||
        "None";

    report +=
        "\n\n";


    report +=
        "MISSING SKILLS\n";

    report +=
        "----------------------------\n";

    report +=
        missingSkills.join(", ") ||
        "None";

    report +=
        "\n\n";


    report +=
        "HIGH PRIORITY MISSING SKILLS\n";

    report +=
        "----------------------------\n";

    report +=
        highMissing.join(", ") ||
        "None";

    report +=
        "\n\n";


    report +=
        "MEDIUM PRIORITY MISSING SKILLS\n";

    report +=
        "----------------------------\n";

    report +=
        mediumMissing.join(", ") ||
        "None";

    report +=
        "\n\n";


    report +=
        "LOW PRIORITY MISSING SKILLS\n";

    report +=
        "----------------------------\n";

    report +=
        lowMissing.join(", ") ||
        "None";

    report +=
        "\n\n";


    report +=
        "IMPROVEMENT SUGGESTIONS\n";

    report +=
        "----------------------------\n";

    report +=
        suggestions.length
            ? suggestions
                .map(
                    item =>
                        `- ${item}`
                )
                .join("\n")
            : "None";

    report +=
        "\n\n";


    report +=
        "RESUME STRENGTHS\n";

    report +=
        "----------------------------\n";

    report +=
        strengths.length
            ? strengths
                .map(
                    item =>
                        `- ${item}`
                )
                .join("\n")
            : "None";

    report +=
        "\n\n";


    report +=
        "AREAS TO IMPROVE\n";

    report +=
        "----------------------------\n";

    report +=
        warnings.length
            ? warnings
                .map(
                    item =>
                        `- ${item}`
                )
                .join("\n")
            : "None";

    report +=
        "\n\n";


    report +=
        "RESUME STATISTICS\n";

    report +=
        "----------------------------\n";

    report +=
        `Word Count: ${analysis.word_count ?? 0}\n`;

    report +=
        `Action Verbs: ${analysis.action_verb_count ?? 0}\n`;

    report +=
        `Quantifiable Achievements: ${analysis.quantifiable_achievement_count ?? 0}\n`;


    const blob =
        new Blob(
            [report],
            {
                type:
                    "text/plain;charset=utf-8"
            }
        );


    const url =
        URL.createObjectURL(
            blob
        );


    const link =
        document.createElement("a");


    const safeName =
        (
            analysis.resume_filename ||
            "resume"
        )
        .replace(
            /\.[^/.]+$/,
            ""
        )
        .replace(
            /[^a-z0-9_-]/gi,
            "_"
        );


    link.href =
        url;


    link.download =
        `${safeName}_analysis_report.txt`;


    document.body.appendChild(
        link
    );


    link.click();


    document.body.removeChild(
        link
    );


    URL.revokeObjectURL(
        url
    );
}


/* =========================================================
   HISTORY
========================================================= */

async function loadHistory() {

    const historyList =
        getElement(
            "historyList"
        );


    if (!historyList) {
        return;
    }


    try {

        const response =
            await fetch(
                `${API_BASE_URL}/analysis/`
            );


        if (!response.ok) {
            throw new Error(
                "Could not load analysis history."
            );
        }


        const data =
            await response.json();


        displayHistory(
            data
        );

    } catch (error) {

        console.error(
            "History error:",
            error
        );


        historyList.innerHTML = `
            <div class="empty-message">
                Unable to load analysis history.
            </div>
        `;
    }
}


/* =========================================================
   DISPLAY HISTORY
========================================================= */

function displayHistory(
    analyses
) {

    const historyList =
        getElement(
            "historyList"
        );


    if (!historyList) {
        return;
    }


    historyList.innerHTML = "";


    if (
        !Array.isArray(analyses) ||
        analyses.length === 0
    ) {

        historyList.innerHTML = `
            <div class="empty-message">
                No previous analyses yet.
            </div>
        `;

        return;
    }


    analyses.forEach(
        analysis => {

            const item =
                document.createElement(
                    "div"
                );


            item.className =
                "history-item";


            const left =
                document.createElement(
                    "div"
                );


            const filename =
                document.createElement(
                    "strong"
                );


            filename.textContent =
                analysis.resume_filename ||
                "Resume";


            const date =
                document.createElement(
                    "span"
                );


            date.textContent =
                formatDate(
                    analysis.created_at
                );


            left.appendChild(
                filename
            );

            left.appendChild(
                date
            );


            const right =
                document.createElement(
                    "div"
                );


            right.className =
                "history-actions";


            const score =
                document.createElement(
                    "span"
                );


            score.className =
                "history-score";


            score.textContent =
                `${normalizeScore(
                    analysis.match_score
                ).toFixed(0)}%`;


            const viewButton =
                document.createElement(
                    "button"
                );


            viewButton.type =
                "button";


            viewButton.textContent =
                "View";


            viewButton.addEventListener(
                "click",
                () =>
                    viewAnalysis(
                        analysis.id
                    )
            );


            const deleteButton =
                document.createElement(
                    "button"
                );


            deleteButton.type =
                "button";


            deleteButton.textContent =
                "Delete";


            deleteButton.className =
                "delete-button";


            deleteButton.addEventListener(
                "click",
                () =>
                    deleteAnalysis(
                        analysis.id
                    )
            );


            right.appendChild(
                score
            );

            right.appendChild(
                viewButton
            );

            right.appendChild(
                deleteButton
            );


            item.appendChild(
                left
            );

            item.appendChild(
                right
            );


            historyList.appendChild(
                item
            );

        }
    );
}


/* =========================================================
   VIEW HISTORY ANALYSIS
========================================================= */

async function viewAnalysis(
    analysisId
) {

    try {

        const response =
            await fetch(
                `${API_BASE_URL}/analysis/${analysisId}`
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Could not load analysis."
            );
        }


        currentAnalysis =
            data;


        displayAnalysis(
            data
        );


        const analysisSection =
            getElement(
                "analysisSection"
            );


        if (analysisSection) {

            analysisSection.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        }


        showStatus(
            "Previous analysis loaded.",
            "success"
        );

    } catch (error) {

        console.error(
            "View analysis error:",
            error
        );


        showStatus(
            error.message ||
            "Could not load analysis.",
            "error"
        );
    }
}


/* =========================================================
   DELETE ANALYSIS
========================================================= */

async function deleteAnalysis(
    analysisId
) {

    const confirmed =
        window.confirm(
            "Delete this analysis?"
        );


    if (!confirmed) {
        return;
    }


    try {

        const response =
            await fetch(
                `${API_BASE_URL}/analysis/${analysisId}`,
                {
                    method: "DELETE"
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Could not delete analysis."
            );
        }


        showStatus(
            "Analysis deleted.",
            "success"
        );


        await loadHistory();

    } catch (error) {

        console.error(
            "Delete error:",
            error
        );


        showStatus(
            error.message ||
            "Could not delete analysis.",
            "error"
        );
    }
}


/* =========================================================
   DELETE ALL ANALYSES
========================================================= */

async function deleteAllAnalyses() {

    const confirmed =
        window.confirm(
            "Are you sure you want to delete all analysis history?"
        );


    if (!confirmed) {
        return;
    }


    try {

        const response =
            await fetch(
                `${API_BASE_URL}/analysis/`,
                {
                    method: "DELETE"
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Could not clear history."
            );
        }


        showStatus(
            "Analysis history cleared.",
            "success"
        );


        await loadHistory();

    } catch (error) {

        console.error(
            "Clear history error:",
            error
        );


        showStatus(
            error.message ||
            "Could not clear history.",
            "error"
        );
    }
}


/* =========================================================
   DATE
========================================================= */

function formatDate(
    value
) {

    if (!value) {
        return "Date unavailable";
    }


    const date =
        new Date(value);


    if (Number.isNaN(
        date.getTime()
    )) {

        return String(value);
    }


    return date.toLocaleString(
        undefined,
        {
            year: "numeric",
            month: "short",
            day: "numeric",

            hour: "numeric",
            minute: "2-digit"
        }
    );
}


/* =========================================================
   FILE INPUT
========================================================= */

function setupFileInput() {

    const fileInput =
        getElement(
            "resumeFile"
        );


    if (!fileInput) {
        return;
    }


    fileInput.addEventListener(
        "change",
        () => {

            uploadedResume =
                null;


            const file =
                fileInput.files[0];


            const selectedFile =
                getElement(
                    "selectedFileName"
                );


            if (!selectedFile) {
                return;
            }


            if (!file) {

                selectedFile.textContent =
                    "";

                return;
            }


            selectedFile.textContent =
                `Selected: ${file.name}`;

        }
    );
}


/* =========================================================
   BUTTON EVENTS
========================================================= */

function setupButtons() {

    const uploadButton =
        getElement(
            "uploadButton"
        );


    const analyzeButton =
        getElement(
            "analyzeButton"
        );


    const downloadButton =
        getElement(
            "downloadReport"
        );


    const clearHistory =
        getElement(
            "clearHistory"
        );


    if (uploadButton) {

        uploadButton.addEventListener(
            "click",
            uploadResume
        );
    }


    if (analyzeButton) {

        analyzeButton.addEventListener(
            "click",
            analyzeResume
        );
    }


    if (downloadButton) {

        downloadButton.addEventListener(
            "click",
            downloadReport
        );
    }


    if (clearHistory) {

        clearHistory.addEventListener(
            "click",
            deleteAllAnalyses
        );
    }
}


/* =========================================================
   INITIALIZE
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        setupFileInput();

        setupButtons();

        loadHistory();

    }
);