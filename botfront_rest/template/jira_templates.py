from jira.resources import Component


issue_template = {
    "issuetype": {
        "name": "$issuetypename"
    },
    "summary": "$summary",
    "description": "$description",
    "project": {
        "key": "$project_key"
    },
    
    "components":[{"name": "$components"}]
            
        
}
