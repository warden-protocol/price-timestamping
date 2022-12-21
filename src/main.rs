use git2::Repository;
use git2::Oid;

extern crate tempdir;

use std::fs;
use std::path::Path;

pub fn test(repo : &Repository, commit: &str, path: Vec<&str>, ur: i32) -> Vec<Oid> {
    let mut oids: Vec<Oid> = vec![];

    let oid: Oid = Oid::from_str(commit).unwrap();
    oids.push(oid);

    let mut commit = repo.find_commit(oid).unwrap();
    for _ in 0..ur {
        commit = commit.parent(0).unwrap();
        oids.push(commit.id());
    }

    let mut id = commit.tree_id();

    for name in path {
        oids.push(id);
        let obj = repo.find_object(id, None).unwrap();

        let tree = obj.into_tree().unwrap();
        let tree_entry = tree.get_name(name).unwrap();
        id = tree_entry.id();
    }
    {
        oids.push(id);
        let obj = repo.find_object(id, None).unwrap();

        let blob = obj.into_blob().unwrap();
        println!("content: {}", String::from_utf8_lossy(blob.content()));
    }
    return oids;
}

pub fn copy(repo : &Repository, new_repo: &Repository, oids: Vec<Oid>) {
    let odb = repo.odb().unwrap();
    let new_odb = new_repo.odb().unwrap();
    for oid in oids.into_iter() {
        let obj = odb.read(oid).unwrap();
        let new_oid = new_odb.write(obj.kind(), obj.data()).unwrap();
        assert!(oid == new_oid);
    }
}

use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();

    let repo_path = args[1].as_str();
    let proof_path = args[2].as_str();


    let commit = args[3].as_str();
    let ur = args[4].parse::<i32>().unwrap();
    let path: Vec<&str> = args[5].split("/").collect();

    let repo = Repository::open(repo_path).unwrap();

    {
        let dir = Path::new(proof_path);
        let _ = fs::remove_dir_all(dir);
        let _ = fs::create_dir(dir);
    }

    let new_repo: Repository =  Repository::init_bare(proof_path).unwrap();

    let oids = test(&repo, commit, path, ur);
    copy(&repo, &new_repo, oids);
}
