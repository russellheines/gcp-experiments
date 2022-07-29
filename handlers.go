package main

import (
	"html/template"
	"net/http"
)

func (pc *PetClinic) listHandler(w http.ResponseWriter, r *http.Request) {
	pets, err := pc.db.list(r.Context())
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	t, err := template.ParseFiles("templates/list.html")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	t.Execute(w, pets)
}

func (pc *PetClinic) detailHandler(w http.ResponseWriter, r *http.Request) {
	id := r.URL.Path[len("/detail/"):]

	t, err := template.ParseFiles("templates/detail.html")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	pet, err := pc.db.get(r.Context(), id)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	t.Execute(w, pet)
}

func (pc *PetClinic) addHandler(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case "GET":
		t, err := template.ParseFiles("templates/add.html")
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		t.Execute(w, nil)
	case "POST":
		imageURL, uploadError := pc.uploadFileFromForm(r)
		if uploadError != nil {
			http.Error(w, uploadError.Error(), http.StatusInternalServerError)
			return
		}

		pet := &Pet{
			Name:     r.FormValue("name"),
			Type:     r.FormValue("type"),
			ImageURL: imageURL,
		}
		pc.db.add(r.Context(), pet)

		http.Redirect(w, r, "/", http.StatusFound)
	}
}

func (pc *PetClinic) editHandler(w http.ResponseWriter, r *http.Request) {
	id := r.URL.Path[len("/edit/"):]
	pet, err := pc.db.get(r.Context(), id)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	switch r.Method {
	case "GET":
		t, err := template.ParseFiles("templates/edit.html")
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		t.Execute(w, pet)
	case "POST":
		imageURL, uploadError := pc.uploadFileFromForm(r)
		if uploadError != nil {
			http.Error(w, uploadError.Error(), http.StatusInternalServerError)
			return
		}

		pet := &Pet{
			ID:       id,
			Name:     r.FormValue("name"),
			Type:     r.FormValue("type"),
			ImageURL: imageURL,
		}

		err := pc.db.edit(r.Context(), pet)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		http.Redirect(w, r, "/", http.StatusFound)
	}
}
