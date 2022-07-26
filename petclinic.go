package main

import (
	"log"
	"net/http"
)

type PetClinic struct {
	db *memoryDB
}

func main() {
	pc := &PetClinic{
		db: newMemoryDB(),
	}

	http.HandleFunc("/", pc.listHandler)
	http.HandleFunc("/detail/", pc.detailHandler)
	http.HandleFunc("/add/", pc.addHandler)
	http.HandleFunc("/edit/", pc.editHandler)

	log.Printf("Listening on localhost:8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal(err)
	}
}
