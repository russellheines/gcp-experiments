package main

import (
	"bytes"
	"io"
	"mime/multipart"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

func TestListHandler(t *testing.T) {
	pc := &PetClinic{
		db: newMemoryDB(),
	}

	req := httptest.NewRequest("GET", "/", nil)
	rec := httptest.NewRecorder()

	pc.listHandler(rec, req)

	resp := rec.Result()
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

	buf := &bytes.Buffer{} // implements io.Reader and io.Writer
	w := multipart.NewWriter(buf)
	w.WriteField("name", "Tom")
	w.Close()

	req := httptest.NewRequest("POST", "/add", buf)
	req.Header.Add("Content-Type", w.FormDataContentType())
	rec := httptest.NewRecorder()

	pc.addHandler(rec, req)

	resp := rec.Result()

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
	rec := httptest.NewRecorder()

	pc.detailHandler(rec, req)

	resp := rec.Result()
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
	rec := httptest.NewRecorder()

	pc.editHandler(rec, req)

	resp := rec.Result()

	if resp.StatusCode != http.StatusInternalServerError {
		t.Error("expected internal server error")
	}
}

func TestEditHandler(t *testing.T) {
	pc := &PetClinic{
		db: newMemoryDB(),
	}

	pc.db.add(&Pet{Name: "Tom", Type: "Fish"})

	buf := &bytes.Buffer{} // implements io.Reader and io.Writer
	w := multipart.NewWriter(buf)
	w.WriteField("name", "Flippy Twitch")
	w.Close()

	req := httptest.NewRequest("POST", "/edit/1", buf)
	req.Header.Add("Content-Type", w.FormDataContentType())
	rec := httptest.NewRecorder()

	pc.editHandler(rec, req)

	resp := rec.Result()

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

	buf := &bytes.Buffer{} // implements io.Reader and io.Writer
	w := multipart.NewWriter(buf)
	w.WriteField("name", "Flippy Twitch")
	w.Close()

	req := httptest.NewRequest("POST", "/edit/2", buf)
	req.Header.Add("Content-Type", w.FormDataContentType())
	rec := httptest.NewRecorder()

	pc.editHandler(rec, req)

	resp := rec.Result()

	if resp.StatusCode != http.StatusInternalServerError {
		t.Error("expected internal server error")
	}
}
