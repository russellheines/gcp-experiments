package main

import (
	"html/template"
	"net/http"
)

func (pc *PetClinic) listHandler(w http.ResponseWriter, r *http.Request) {
	pets := pc.db.list()

	t, err := template.ParseFiles("templates/list.html")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}

	t.Execute(w, pets)
}

func (pc *PetClinic) detailHandler(w http.ResponseWriter, r *http.Request) {
	id := r.URL.Path[len("/detail/"):]

	t, err := template.ParseFiles("templates/detail.html")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}

	pet, err := pc.db.get(id)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}

	t.Execute(w, pet)
}

func (pc *PetClinic) addHandler(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case "GET":
		t, err := template.ParseFiles("templates/add.html")
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
		}
		t.Execute(w, nil)
	case "POST":
		pet := &Pet{
			Name: r.FormValue("name"),
			Type: r.FormValue("type"),
		}
		pc.db.add(pet)

		http.Redirect(w, r, "/", http.StatusFound)
	}
}

func (pc *PetClinic) editHandler(w http.ResponseWriter, r *http.Request) {
	id := r.URL.Path[len("/edit/"):]
	pet, err := pc.db.get(id)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}

	switch r.Method {
	case "GET":
		t, err := template.ParseFiles("templates/edit.html")
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
		}
		t.Execute(w, pet)
	case "POST":
		pet := &Pet{
			ID:   id,
			Name: r.FormValue("name"),
			Type: r.FormValue("type"),
		}
		err := pc.db.edit(pet)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
		}

		http.Redirect(w, r, "/", http.StatusFound)
	}
}
