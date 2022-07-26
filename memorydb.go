package main

import (
	"errors"
	"sort"
	"strconv"
)

type Pet struct {
	ID   string
	Name string
	Type string
}

type memoryDB struct {
	nextID int64
	pets   map[string]*Pet
}

func newMemoryDB() *memoryDB {
	return &memoryDB{
		nextID: 1,
		pets:   make(map[string]*Pet),
	}
}

func (db *memoryDB) list() []*Pet {

	var pets []*Pet
	for _, p := range db.pets {
		pets = append(pets, p)
	}

	sort.Slice(pets, func(i, j int) bool {
		return pets[i].Name < pets[j].Name
	})

	return pets
}

func (db *memoryDB) add(p *Pet) {
	p.ID = strconv.FormatInt(db.nextID, 10)
	db.pets[p.ID] = p
	db.nextID++
}

func (db *memoryDB) get(id string) (*Pet, error) {
	_, ok := db.pets[id]
	if !ok {
		return nil, errors.New("pet not found")
	}

	return db.pets[id], nil
}

func (db *memoryDB) edit(p *Pet) error {
	if p.ID == "" {
		return errors.New("missing pet id")
	}
	db.pets[p.ID] = p

	return nil
}

func (db *memoryDB) delete(id string) error {
	_, ok := db.pets[id]
	if !ok {
		return errors.New("pet not found")
	}

	delete(db.pets, id)

	return nil
}
