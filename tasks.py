from invoke import task, Collection
import os
import shutil
import uuid
from git import Repo
import datetime
import filecmp

dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
repo_path = os.path.join(dir_path, "cvtemp")
cc_project_name = "cv_repo"
repo_url = "https://github.com/msalvaris/AKS-Deployment-for-Image-Classification"


@task
def cv_project(c):
    """Create CV project from cookiecutter
    """
    with c.cd(dir_path):
        c.run(
            f"cookiecutter cvbpcc --no-input type=cv project_name={cc_project_name}",
            pty=True,
        )
    _fake_update(os.path.join(dir_path, cc_project_name))


def _fake_update(repo_path):
    with open(os.path.join(repo_path, "04_flask_deployment.ipynb"), "a") as f:
        f.writelines("Additional content")


@task
def clean(c):
    """Clean project
    """
    with c.cd(dir_path):
        c.run(f"rm -r {cc_project_name}", pty=True)


def _get_random_id():
    return uuid.uuid4()


@task
def clean_temp_repo(c):
    try:
        shutil.rmtree(repo_path)
    except FileNotFoundError:
        print("Did not delete")


def _update_project(
    context, repo, origin_branch, pr_branch_name, new_branch, commit_msg, pr_msg
):
    generated_project_path = os.path.join(dir_path, cc_project_name)
    comparison_results = filecmp.dircmp(generated_project_path, repo_path)

    if len(comparison_results.diff_files) > 0:
        print("Files are different updating project")
        # copy files
        print(
            f"Copying files from {generated_project_path} to {repo_path} branch {pr_branch_name}"
        )
        context.run(f"cp -r {generated_project_path}/* {repo_path}/")

        print("Commiting updates")
        repo.git.commit("-am", commit_msg)
        print("Pushing updates")
        repo.git.push("origin", new_branch)

        print("Creating pull request")
        with context.cd(repo_path):
            context.run(f"hub pull-request -m '{pr_msg}' -b {origin_branch}", pty=True)
    else:
        print("Files are the same no need to update")


@task(pre=[cv_project], post=[clean_temp_repo, clean])
def update(c, id=None):
    """Update projects based on template
    
    Args:
        id (string, optional): Extra identifier to be added to update branch name. Defaults to random uuid.
    """
    if id is None:
        id = _get_random_id()
        print(f"Generating random branch id {id}")

    today_str = datetime.date.today().strftime("%B %d, %Y")
    origin_branch = "staging"
    pr_branch_name = f"branch_{id}"
    commit_msg = "Updating notebooks from automated cookiecutter build"
    pr_msg = f"Update from automated system on {today_str}"

    print("Cloning")
    r = Repo.clone_from(repo_url, repo_path, branch=origin_branch)

    print(f"Creating branch {pr_branch_name}")
    new_branch = r.create_head(pr_branch_name)
    new_branch.checkout()

    _update_project(c, r, origin_branch, pr_branch_name, new_branch, commit_msg, pr_msg)


namespace = Collection(cv_project, clean, update, clean_temp_repo)

