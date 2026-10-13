from common import RACINE, load_test
df = load_test()
(RACINE / "data_clean").mkdir(exist_ok=True)
df.to_csv(RACINE / "data_clean" / "test_clean.csv", index=False)
print(df.shape)




