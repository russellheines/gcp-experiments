package main

import (
	"io"
	"net/http"
	"net/http/httptest"
	"net/url"
	"strings"
	"testing"
)

func TestListHandler(t *testing.T) {
	pc := &PetClinic{
		db: newMemoryDB(),
	}

	req := httptest.NewRequest("GET", "/", nil)
	w := httptest.NewRecorder()

	pc.listHandler(w, req)

	resp := w.Result()
	body, _ := io.ReadAll(resp.Body)

	if resp.StatusCode != http.StatusOK {
		t.Error("expected ok")
	}
	if !strings.Contains(string(body), "No pets found") {
		t.Error("expected \"No pets found\"")
	}
}

func TestAddHandler(t *testing.T) {
	pc := &PetClinic{
		db: newMemoryDB(),
	}

	data := url.Values{}
	data.Set("name", "Tom")
	data.Set("type", "Fish")

	req := httptest.NewRequest("POST", "/add", strings.NewReader(data.Encode()))
	req.Header.Add("Content-Type", "application/x-www-form-urlencoded")
	w := httptest.NewRecorder()

	pc.addHandler(w, req)

	resp := w.Result()

	if resp.StatusCode != http.StatusFound {
		t.Error("expected redirect")
	}
	if len(pc.db.list()) != 1 {
		t.Error("expected one pet")
	}
}

func TestDetailHandler(t *testing.T) {
	pc := &PetClinic{
		db: newMemoryDB(),
	}

	pc.db.add(&Pet{Name: "Flippy Twitch", Type: "Fish"})

	req := httptest.NewRequest("POST", "/detail/1", nil)
	w := httptest.NewRecorder()

	pc.detailHandler(w, req)

	resp := w.Result()
	body, _ := io.ReadAll(resp.Body)

	if resp.StatusCode != http.StatusOK {
		t.Error("expected ok")
	}
	if !strings.Contains(string(body), "Flippy Twitch") {
		t.Error("expected \"Flippy Twitch\"")
	}
}

func TestDetailHandler_InternalServerError(t *testing.T) {
	pc := &PetClinic{
		db: newMemoryDB(),
	}

	req := httptest.NewRequest("GET", "/detail/2", nil)
	w := httptest.NewRecorder()

	pc.editHandler(w, req)

	resp := w.Result()

	if resp.StatusCode != http.StatusInternalServerError {
		t.Error("expected internal server error")
	}
}

func TestEditHandler(t *testing.T) {
	pc := &PetClinic{
		db: newMemoryDB(),
	}

	pc.db.add(&Pet{Name: "Tom", Type: "Fish"})

	data := url.Values{}
	data.Set("name", "Flippy Twitch")
	data.Set("type", "Fish")

	req := httptest.NewRequest("POST", "/edit/1", strings.NewReader(data.Encode()))
	req.Header.Add("Content-Type", "application/x-www-form-urlencoded")
	w := httptest.NewRecorder()

	pc.editHandler(w, req)

	resp := w.Result()

	if resp.StatusCode != http.StatusFound {
		t.Error("expected ok")
	}
	if p, _ := pc.db.get("1"); p.Name != "Flippy Twitch" {
		t.Error("Flippy Twitch")
	}
}

func TestEditHandler_InternalServerError(t *testing.T) {
	pc := &PetClinic{
		db: newMemoryDB(),
	}

	req := httptest.NewRequest("POST", "/edit/2", nil)
	w := httptest.NewRecorder()

	pc.editHandler(w, req)

	resp := w.Result()

	if resp.StatusCode != http.StatusInternalServerError {
		t.Error("expected internal server error")
	}
}
