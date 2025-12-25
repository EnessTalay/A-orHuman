namespace aıorhumanv2.Models
{
    public class TahminViewModel
    {
        public string? Metin { get; set; }
        public string? FinalPrediction { get; set; }
        public int? FinalAiPercent { get; set; }
        public int? FinalHumanPercent { get; set; }
        public string? HataMesaji { get; set; }
        public string? Tahmin { get; set; }
        public string? KullanilanModel { get; set; }

        public ModelDetail Lr { get; set; } = new();
        public ModelDetail Svm { get; set; } = new();
        public ModelDetail Nb { get; set; } = new();
    }

    public class ModelDetail
    {
        public string? Prediction { get; set; }
        public int? AiPercent { get; set; }
    }

    public class TahminSonucu
    {
        public string? prediction { get; set; }
        public string? model_used { get; set; }
    }
}