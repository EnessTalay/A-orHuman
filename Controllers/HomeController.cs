using System.Text;
using System.Text.Json;
using Microsoft.AspNetCore.Mvc;
using aıorhumanv2.Models;

namespace aıorhumanv2.Controllers;

public class HomeController : Controller
{
    private readonly IHttpClientFactory _httpClientFactory;

    public HomeController(IHttpClientFactory httpClientFactory)
    {
        _httpClientFactory = httpClientFactory;
    }

    public IActionResult Index() => View(new TahminViewModel());

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Index(TahminViewModel model)
    {
        if (string.IsNullOrWhiteSpace(model.Metin))
        {
            model.HataMesaji = "Lütfen bir metin girin.";
            return View(model);
        }

        try
        {
            var client = _httpClientFactory.CreateClient();
            var payload = new { text = model.Metin };
            var json = JsonSerializer.Serialize(payload);
            var content = new StringContent(json, Encoding.UTF8, "application/json");

            var response = await client.PostAsync("http://127.0.0.1:8000/predict", content);
            if (!response.IsSuccessStatusCode) throw new Exception();

            var responseJson = await response.Content.ReadAsStringAsync();
            using var doc = JsonDocument.Parse(responseJson);
            var root = doc.RootElement;

            model.FinalPrediction = root.GetProperty("final_prediction").GetString();
            model.FinalAiPercent = root.GetProperty("final_ai_percent").GetInt32();
            model.FinalHumanPercent = 100 - model.FinalAiPercent;

            var mod = root.GetProperty("models");
            model.Lr.AiPercent = mod.GetProperty("lr").GetProperty("ai_percent").GetInt32();
            model.Svm.AiPercent = mod.GetProperty("svm").GetProperty("ai_percent").GetInt32();
            model.Nb.AiPercent = mod.GetProperty("nb").GetProperty("ai_percent").GetInt32();

            return View(model);
        }
        catch
        {
            model.HataMesaji = "Bağlantı Hatası: API Açık mı?";
            return View(model);
        }
    }
}