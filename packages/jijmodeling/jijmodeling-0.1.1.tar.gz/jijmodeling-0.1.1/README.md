# Jij-Modeling

## 仮想環境の設定
```
$ pipenv update
$ pipenv shell
```
これでpipenv で記述されている必要な仮想環境に入る。

## テストの実行

`tests` 以下の全てのテストファイルの実行
```
$ python -m unittest discover tests
```

## Deployについて

2020/8/24 時点では Azure DevOps の Artifacts に Publicでデプロイしている。

https://dev.azure.com/jijinc/jij-cloud-public

ここへアクセスしてArtifactsを見て欲しい。何も見えない場合は、Jijの他の開発者に聞いて招待してもらって欲しい。

まずパッケージをまとめる。

```shell
python setup.py sdist
```

通常のPyPIへのデプロイと同じように twine を利用するが、Azureアカウントの認証のためのライブラリを入れる必要がある。

```shell
pip install artifacts-keyring --pre
```

そうすると

```shell
twine upload --repository-url https://pkgs.dev.azure.com/jijinc/_packaging/jijcloud/pypi/upload dist/*
```

でアップロードできるはずである。


## 内部設計


数式を木構造で構築していく。

ルートノードは数理モデル自体.  
レイヤーはCost と各制約条件.
その次のレイヤーからが数式情報. 

数式(Term)は
```
Operator, Coefficient, Term, constant, exponent
```
という構成になっていてTermの入子構造になっている。

また Term は足（添字）を持ち、Operator は総和のような演算を行う。


木の一番端の葉の部分には Tensor クラスを継承した、変数などのプレースホルダーが存在する。

また、Tensorクラスを継承しているクラスは同時にVariableクラス（インターフェース）を継承する。
各プレースホルダーはVariableインターフェースのメソッドを使って、その変数が、最適化変数なのか、データのための変数なのかなどの情報を持ちます。

## 最適化計算において必要な要素

- 最適化変数
- データを表す変数
- 未定乗数などモデルに関わる変数
- テンソル構造（添字構造）
- 添字に対する演算子

## Variable クラス

## Tensor クラス

Jij-Modeling の大元.

添字をもつクラスは全てこのTensorクラスを継承する。

Tensorクラスは添字のラベルが確定していない状態。

## Operator クラス

メンバ変数にTermクラスをもつ